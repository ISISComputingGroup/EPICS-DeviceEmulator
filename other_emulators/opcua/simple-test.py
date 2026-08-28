import asyncio
import logging

from asyncua import Server, ua
from asyncua.common.methods import uamethod


@uamethod
def func(parent, value):
    return value * 2


async def main():
    _logger = logging.getLogger(__name__)
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840")

    # set up our own namespace, not really necessary but should as spec
    uri = "http://isiscomputing-namespace.epics"
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    print(type(idx), idx)
    myobj = await server.nodes.objects.add_object(idx, bname="Pressure_Values")
    pressure_var = await myobj.add_variable(idx, "Pressure", 6.7)
    temp_var = await myobj.add_variable(idx, "Temperature", 30.5)
    # Set Pressure and Temperature to be writable by clients
    await pressure_var.set_writable()
    await temp_var.set_writable()
    await server.nodes.objects.add_method(
        ua.NodeId("ServerMethod", idx),
        ua.QualifiedName("ServerMethod", idx),
        func,
        [ua.VariantType.Int64],
        [ua.VariantType.Int64],
    )
    _logger.info("Starting server!")

    print(f"Pressure NodeId: {pressure_var.nodeid}")
    print(f"Temperature NodeId: {temp_var.nodeid}")
    async with server:
        while True:
            await asyncio.sleep(1)
            new_val = await pressure_var.get_value() + 0.1
            new_val2 = await temp_var.get_value() + 0.05
            _logger.info("Set value of %s to %.1f", pressure_var, new_val)
            _logger.info("Set value of %s to %.1f", temp_var, new_val2)
            await pressure_var.write_value(new_val)
            await temp_var.write_value(new_val2)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=False)