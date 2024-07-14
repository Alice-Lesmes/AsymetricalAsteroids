package com.example.asymetricasteroids

import net.razorvine.pickle.Pickler
import net.razorvine.pickle.Unpickler
import java.net.Socket

class Client(addr : String, port: Int) {
    // Needs to be changed depending on the threadedServer.py
    val SERVER_ADDRESS = addr
    val SERVER_PORT = port

    fun connect(data: Data) {
        // THis doesn't work, prob cause something on threadedServer.py
        val connected = true
        println("Getting Client")
        var client = Socket(SERVER_ADDRESS, SERVER_PORT)     // The connection to server
        println("Connected to " + client)
        // Continuously check
        while (connected)
        {
            var reply = "Hello!"
            var pickler = Pickler()     // Allows to pickle data
            var unpickler = Unpickler()     // Allows to unpickle data
            var received_data = unpickler.load(client.getInputStream())
            client.outputStream.write(pickler.dumps(reply))     // Send back data
            println("Receiving: " + unpickler.load(client.getInputStream()))

            if (received_data.toString() == "")
            {
                client.close()
                break
            }
        }
    }

    fun formatReply(data: Data) : String
    {
        // Just manually creating essentially JSON, but in a string
        // The modules are just the
        var modulesArray = arrayOf("O2", "Engines", "Radar")
        var modules = "'modules': {"
        for (module in modulesArray)
        {
            modules += "'$module': ${data.getPower(module)}, "
        }
        modules = modules.removeSuffix(", ")
        modules += "}, "

        var weaponData = "'weapon': '${data.getWeaponElement()}'"
        var reply : String = "{$modules, $weaponData}"
        return reply
    }
}