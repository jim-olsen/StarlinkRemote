import grpc
import math
import json
import statistics
from PIL import Image
import yagrc.reflector
import numpy as np
import time

try:
    from yagrc import importer

    importer.add_lazy_packages(["spacex.api.device"])
except (ImportError, AttributeError):
    print("Error importing lazy packages")

from spacex.api.device import device_pb2
from spacex.api.device import device_pb2_grpc
from spacex.api.device import dish_pb2


#
# This class provides all of the dish oriented instructions for communicating with the gRPC available interfaces.  Each
# of the methods tries to abstract the data into more usable forms for simple programmatic access rather than the
# lower level formats of the raw calls.  This class is in no way all inclusive, but will grow as more features are
# discovered.
#
class Starlink:
    starlinkurl = None

    #
    # url - The url to which we should connect to the dish.  The default provided value is likely what it should be
    # unless you have setup some kind of alternative static route
    #
    def __init__(self, url="192.168.100.1:9200"):
        if url is not None:
            self.starlinkurl = url
        with grpc.insecure_channel(self.starlinkurl) as channel:
            importer.resolve_lazy_imports(channel)

    #
    # return a status structure containing the values from a get_status request to the gRPC service.  This data has
    # been simplified into a structure that is more readily consumable by a ui or a web client
    #
    def get_status(self):
        with grpc.insecure_channel(self.starlinkurl) as channel:
            stub = device_pb2_grpc.DeviceStub(channel)
            response = stub.Handle(device_pb2.Request(get_status={}), timeout=10)
            result = response.dish_get_status

        status = {}

        # Connection State
        if result.HasField("outage"):
            if result.outage.cause == dish_pb2.DishOutage.Cause.NO_SCHEDULE:
                status["state"] = "SEARCHING"
            else:
                status["state"] = dish_pb2.DishOutage.Cause.Name(result.outage.cause)
        else:
            status["state"] = "CONNECTED"

        # Alerts
        alerts = {}
        for field in result.alerts.DESCRIPTOR.fields:
            alerts[field.name] = getattr(result.alerts, field.name)
        status["alerts"] = alerts

        # Obstruction Stats
        if not math.isnan(result.obstruction_stats.avg_prolonged_obstruction_duration_s) and not math.isnan(
                result.obstruction_stats.avg_prolonged_obstruction_interval_s):
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
        status["ready_states"] = {"cady": result.ready_states.cady,
                                  "scp": result.ready_states.scp,
                                  "l1l2": result.ready_states.l1l2,
                                  "xphy": result.ready_states.xphy,
                                  "aap": result.ready_states.aap,
                                  "rf": result.ready_states.rf}

        return status

    #
    # This method returns a single instance of a history object that contains the history for a specific kind of
    # statistic, such as ping latency, or download mbps.  It also calculates standard statistical summary data for
    # all of the values contained within the run of historical data stored.  This allows us to examine such things as
    # mean, min, max of the data over the time period recorded.  It does not cover longer term historical data.
    #
    def get_history_object(self, source, field, target_name):
        result = {}
        result[target_name] = []
        total_val = 0.0
        maximum_val = 0.0
        minimum_val = float("inf")
        samples = getattr(source, field)
        num_samples = len(samples)
        loop_end = int(source.current) % num_samples
        for i in range(num_samples):
            value = samples[(loop_end + 1 + i) % num_samples]
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

    #
    # Returns a record containing all the available historical data in the dish.  The dish at the time of writing
    # only stores the last 900 seconds of data for each of these fields.  It also stores the last 12 hours of outage
    # data.  Note that these outages will include ones that are less than 2 seconds in duration.  It also summarizes
    # the outage data into buckets to look at the occurrences of outages by type.
    #
    def get_history(self):
        with grpc.insecure_channel(self.starlinkurl) as channel:
            stub = device_pb2_grpc.DeviceStub(channel)
            response = stub.Handle(device_pb2.Request(get_history={}), timeout=10)
            result = response.dish_get_history

        history = {}
        history["current"] = result.current
        history.update(self.get_history_object(result, "pop_ping_drop_rate", "ping_drop_rate"))
        history.update(self.get_history_object(result, "pop_ping_latency_ms", "ping_latency"))
        history.update(self.get_history_object(result, "downlink_throughput_bps", "downlink_bps"))
        history.update(self.get_history_object(result, "uplink_throughput_bps", "uplink_bps"))

        history["outages"] = []
        total_outages = 0
        total_seconds = 0.0
        cause_enum = dish_pb2.DishOutage.Cause
        outages_by_category = {}
        for key in cause_enum.keys():
            outages_by_category[key] = 0
        for outage in result.outages:
            history["outages"].append(
                {"cause": dish_pb2.DishOutage.Cause.Name(outage.cause), "start_timestamp": outage.start_timestamp_ns,
                 "duration": outage.duration_ns / 1000000000, "did_switch": outage.did_switch})
            outages_by_category[dish_pb2.DishOutage.Cause.Name(outage.cause)] += 1
            total_outages += 1
            total_seconds += (outage.duration_ns / 1000000000)
        history["total_outages"] = total_outages
        history["total_outage_seconds"] = total_seconds
        history["average_outage_seconds"] = total_seconds / len(history["outages"])
        history["outages_by_category"] = outages_by_category

        return history

    #
    # This method returns the raw SNR outage map data.  This data includes a 100x100 table view of the SNR values that
    # the dish has encountered.  Places it has not yet gotten data for will be a value of -1.0, while the other values
    # will be between 0.0 and 1.0, with 1.0 being the strongest signal.
    #
    def get_obstruction_map_data(self):
        with grpc.insecure_channel(self.starlinkurl) as channel:
            stub = device_pb2_grpc.DeviceStub(channel)
            response = stub.Handle(device_pb2.Request(dish_get_obstruction_map={}), timeout=10)
            result = response.dish_get_obstruction_map

        return tuple(
            (result.snr[i:i + result.num_cols]) for i in range(0, result.num_cols * result.num_rows, result.num_cols))

    #
    # Takes two obstruction maps, and calculates the difference between them.  This allows you to examine two
    # obstructions maps from two different period of time, and turn it into an image where newly seen signals are green.
    # By doing this, you can see the satellite paths in green of new 'hits' on satellites.  Note that this only works
    # on new data that is either a stronger signal than previously seen, or an unseen value.  This works well if you
    # reboot the dish so all signal values are cleared.  On a dish with a fully populated obstruction map, you will see
    # very little change.
    #
    def get_obstruction_map_differences(self, obstruction_map, baseline_obstruction_map):
        image_array = []
        for y, row in enumerate(obstruction_map):
            image_array.append([None] * len(row))
            for x, value in enumerate(row):
                if value != baseline_obstruction_map[y][x]:
                    image_array[y][x] = [0x00, 0xFF, 0x00]
                    print("Value at " + str(y) + "," + str(x) + " has change from " + str(
                        baseline_obstruction_map[y][x]) + " to " + str(value))
                else:
                    if value == -1:
                        image_array[y][x] = [0x00, 0x00, 0x00]
                    else:
                        image_array[y][x] = [0xAD, 0xD8, 0xE6]

        return image_array

    #
    # Fetch the obstruction map data from the dish, and populate it into an obstruction map image array.  This will be
    # a series of RGB pixels that can then be displayed as the obstruction map itself.  See the main function below for
    # an example of how to turn it into a png
    #
    def get_obstruction_map(self):
        map_data = self.get_obstruction_map_data()

        image_array = []
        for y, image_row in enumerate(map_data):
            image_array.append([None] * len(image_row))
            for x, snr_value in enumerate(image_row):
                if snr_value > 1.0:
                    # shouldn't happen, but just in case...
                    snr_value = 1.0
                # if we have a valid SNR reading
                if snr_value >= 0.0:
                    # if snr is above 0.5, mark it as blue (unobstructed)
                    if snr_value >= 0.5:
                        image_array[y][x] = [0xAD, 0xD8, 0xE6]
                    # otherwise mark it as red (obstructed)
                    else:
                        image_array[y][x] = [0xFF, 0x00, 0x00]
                # otherwise we have no value so mark it as black (no data)
                else:
                    image_array[y][x] =  [0x00, 0x00, 0x00]
        return image_array

    #
    # Issue the command to ask the dish to stow itself
    #
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

    #
    # Issue the command to ask the dish to unstow itself
    #
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

    #
    # Issue the command to ask the dish to reboot itself
    #
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

#
# If you just run this class instead of the server.py file that actually runs the flask server, run through each command
# to test that it works.  stow/unstow are commented out by default as we don't want to accidentally run those unless you
# really want to do that.
#
def main():
    starlink = Starlink()
    status = starlink.get_status()
    print(json.dumps(status, indent=3))
    history = starlink.get_history()
    print(json.dumps(history, indent=3))
    obstruction_map = starlink.get_obstruction_map_data()
    print(json.dumps(obstruction_map, indent=3))

    obstruction_image = starlink.get_obstruction_map()
    numpy_image = np.array(obstruction_image).astype('uint8')
    img = Image.fromarray(numpy_image)
    img.show()

    obstruction_data_baseline = starlink.get_obstruction_map_data()
    #    time.sleep(60 * 5)
    obstruction_data = starlink.get_obstruction_map_data()
    obstruction_image = starlink.get_obstruction_map_differences(obstruction_data, obstruction_data_baseline)
    numpy_image = np.array(obstruction_image).astype('uint8')
    img = Image.fromarray(numpy_image)
#    img.show()

#    starlink.dish_stow()
#    starlink.dish_unstow()


if __name__ == '__main__':
    main()
