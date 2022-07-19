import grpc
import math
import json
import statistics

import yagrc.reflector

try:
    from yagrc import importer
    importer.add_lazy_packages(["spacex.api.device"])
except (ImportError, AttributeError):
    print("Error importing lazy packages")

from spacex.api.device import device_pb2
from spacex.api.device import device_pb2_grpc
from spacex.api.device import dish_pb2

class Starlink:
    starlinkurl = None

    def __init__(self, url="192.168.100.1:9200"):
        if url is not None:
            self.starlinkurl = url
        with grpc.insecure_channel(self.starlinkurl) as channel:
            importer.resolve_lazy_imports(channel)

    def get_status(self):
        with grpc.insecure_channel(self.starlinkurl) as channel:
            stub = device_pb2_grpc.DeviceStub(channel)
            response = stub.Handle(device_pb2.Request(get_status={}), timeout=10)
            result = response.dish_get_status

        status = {}

        # Connection State
        if result.HasField("outage"):
            if result.outage.cause == dish_pb2.DisOutage.Cause.NO_SCHEDULE:
                status["state"] = "SEARCHING"
            else:
                status["state"] = dish_pb2.DisOutage.Cause.Name(result.outage.cause)
        else:
            status["state"] = "CONNECTED"

        # Alerts
        alerts = {}
        for field in result.alerts.DESCRIPTOR.fields:
            alerts[field.name] = getattr(result.alerts, field.name)
        status["alerts"] = alerts

        # Obstruction Stats
        if not math.isnan(result.obstruction_stats.avg_prolonged_obstruction_duration_s) and not math.isnan(result.obstruction_stats.avg_prolonged_obstruction_interval_s):
            status["obstruction_duration_avg"] = result.obstruction_stats.avg_prolonged_obstruction_duration_s
            status["obstruction_interval_avg"] = result.obstruction_stats.avg_prolonged_obstruction_interval_s

        status["id"] = result.device_info.id
        status["hardware_version"] = result.device_info.hardware_version
        status["software_version"] = result.device_info.software_version
        status["country_code"] = result.device_info.country_code
        status["utc_offset"] = result.device_info.utc_offset_s
        status["bootcount"] = result.device_info.bootcount
        status["uptime"] = result.device_state.uptime_s
        status["gps_valid"] = result.gps_stats.gps_valid
        status["gps_sats"] = result.gps_stats.gps_sats
        status["downlink_throughput_bps"] = result.downlink_throughput_bps
        status["uplink_throughput_bps"] = result.uplink_throughput_bps
        status["fraction_obstructed"] = result.obstruction_stats.fraction_obstructed
        status["obstruction_valid"] = result.obstruction_stats.valid_s
        status["boresight_azimuth"] = result.boresight_azimuth_deg
        status["boresight_elevation"] = result.boresight_elevation_deg
        status["ethernet_speed"] = result.eth_speed_mbps
        status["snr_above_noise_floor"] = result.is_snr_above_noise_floor
        status["cady_ready"] = result.ready_states.cady
        status["scp_ready"] = result.ready_states.scp
        status["l1l2_ready"] = result.ready_states.l1l2
        status["xphy_ready"] = result.ready_states.xphy
        status["aap_ready"] = result.ready_states.aap
        status["rf_ready"] = result.ready_states.rf

        return status

    def get_history_object(self, source, field, target_name):
        result = {}
        result[target_name] = []
        total_val = 0.0
        maximum_val = 0.0
        minimum_val = float("inf")
        for value in getattr(source, field):
            if value < minimum_val:
                minimum_val = value
            if value > maximum_val:
                maximum_val = value
            total_val += value
            result[target_name].append(value)
        result["average_" + target_name] = total_val / len(result[target_name])
        result["minimum_" + target_name] = minimum_val
        result["maximum_" + target_name] = maximum_val
        result["median_" + target_name] = statistics.median(result[target_name])

        return result

    def get_history(self):
        with grpc.insecure_channel(self.starlinkurl) as channel:
            stub = device_pb2_grpc.DeviceStub(channel)
            response = stub.Handle(device_pb2.Request(get_history={}), timeout=10)
            result = response.dish_get_history

        history = {}
        history.update(self.get_history_object(result, "pop_ping_drop_rate", "ping_drop_rate"))
        history.update(self.get_history_object(result, "pop_ping_latency_ms", "ping_latency"))
        history.update(self.get_history_object(result, "downlink_throughput_bps", "downlink_bps"))
        history.update(self.get_history_object(result, "uplink_throughput_bps", "uplink_bps"))

        history["outages"] = []
        total_outages = 0
        total_seconds = 0.0
        cause_enum = dish_pb2.DishOutage.Cause

        for outage in result.outages:
            history["outages"].append({"cause": dish_pb2.DishOutage.Cause.Name(outage.cause), "start_timestamp": outage.start_timestamp_ns,
                                       "duration": outage.duration_ns / 1000000000, "did_switch": outage.did_switch})
            key_name = "total_" + dish_pb2.DishOutage.Cause.Name(outage.cause) + "_outages"
            if not key_name in history:
                history[key_name] = 1
            else:
                history[key_name] += 1
            total_outages += 1
            total_seconds += (outage.duration_ns / 1000000000)
        history["total_outages"] = total_outages
        history["total_outage_seconds"] = total_seconds
        history["average_outage_seconds"] = total_seconds / len(history["outages"])

        return history

    def get_obstruction_map(self):
        with grpc.insecure_channel(self.starlinkurl) as channel:
            stub = device_pb2_grpc.DeviceStub(channel)
            response = stub.Handle(device_pb2.Request(dish_get_obstruction_map={}), timeout=10)
            result = response.dish_get_obstruction_map

        obstruction_map = {}
        return obstruction_map

    def dish_stow(self):
        reflector = yagrc.reflector.GrpcReflectionClient()
        try:
            with grpc.insecure_channel(self.starlinkurl) as channel:
                reflector.load_protocols(channel, symbols=["SpaceX.API.Device.Device"])
                request_class = reflector.message_class("SpaceX.API.Device.Request")
                request = request_class(dish_stow={})
                stub = reflector.service_stub_class("SpaceX.API.Device.Device")(channel)
                response = stub.Handle(request, timeout=120)
                return True
        except grpc.RpcError as e:
            if (isinstance(e, grpc.Call)):
                print("Failed to stow dish: " + e.details())
            else:
                print("Failed to stow dish for an unknown reason")

        return False

    def dish_unstow(self):
        reflector = yagrc.reflector.GrpcReflectionClient()
        try:
            with grpc.insecure_channel(self.starlinkurl) as channel:
                reflector.load_protocols(channel, symbols=["SpaceX.API.Device.Device"])
                request_class = reflector.message_class("SpaceX.API.Device.Request")
                request = request_class(dish_stow={"unstow": True})
                stub = reflector.service_stub_class("SpaceX.API.Device.Device")(channel)
                response = stub.Handle(request, timeout=120)
                return True
        except grpc.RpcError as e:
            if (isinstance(e, grpc.Call)):
                print("Failed to unstow dish: " + e.details())
            else:
                print("Failed to unstow dish for an unknown reason")

        return False

    def dish_reboot(self):
        reflector = yagrc.reflector.GrpcReflectionClient()
        try:
            with grpc.insecure_channel(self.starlinkurl) as channel:
                reflector.load_protocols(channel, symbols=["SpaceX.API.Device.Device"])
                request_class = reflector.message_class("SpaceX.API.Device.Request")
                request = request_class(reboot={})
                stub = reflector.service_stub_class("SpaceX.API.Device.Device")(channel)
                response = stub.Handle(request, timeout=120)
                return True
        except grpc.RpcError as e:
            if (isinstance(e, grpc.Call)):
                print("Failed to reboot dish: " + e.details())
            else:
                print("Failed to reboot dish for an unknown reason")

        return False


def main():
    starlink = Starlink()
    status = starlink.get_status()
    print(json.dumps(status, indent=3))
    history = starlink.get_history()
    print(json.dumps(history, indent=3))
    obstruction_map = starlink.get_obstruction_map()
    print(json.dumps(obstruction_map, indent=3))


if __name__ == '__main__':
    main()

