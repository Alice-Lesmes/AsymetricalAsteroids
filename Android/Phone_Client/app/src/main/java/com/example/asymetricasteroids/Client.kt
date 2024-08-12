package com.example.asymetricasteroids

import io.ktor.network.selector.SelectorManager
import io.ktor.network.sockets.aSocket
import io.ktor.network.sockets.openReadChannel
import io.ktor.network.sockets.openWriteChannel
import io.ktor.utils.io.core.readBytes
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import net.razorvine.pickle.Pickler
import net.razorvine.pickle.Unpickler
import java.net.Socket
import kotlin.system.exitProcess

class Client(data: Data) {
    // Needs to be changed depending on the threadedServer.py
    var SERVER_ADDRESS = "192.168.x.x"  // Dummy address
    var SERVER_PORT = 8000  // Realistically we would keep it on this port
    var pickler = Pickler()     // Allows to pickle data
    var unpickler = Unpickler()     // Allows to unpickle data
    var data =  data
    fun ktorMain()
    {
        runBlocking {
            val selectorManager = SelectorManager(Dispatchers.IO)
            val socket = aSocket(selectorManager).tcp().connect(SERVER_ADDRESS, SERVER_PORT)

            val receiveChannel = socket.openReadChannel()
            val sendChannel = socket.openWriteChannel(autoFlush = true)

            launch(Dispatchers.IO) {
                while (true) {
                    val greeting = receiveChannel.readPacket(0).readBytes(0)

                    if (greeting != null) {
                    } else {
                        println("Server closed a connection")
                        socket.close()
                        selectorManager.close()
                        exitProcess(0)
                    }
                }
            }

            while (true) {
                val myMessage = pickler.dumps("Hello from android")
                sendChannel.write { myMessage }
            }
        }

    }
    // Suspend so it can be run without blocking main(UI) thread
    // Allows for coroutine
    suspend fun connect() = coroutineScope {
        // Not sure why *Everything* needs be in 'launch' but it works this way
        launch {
            val connected = true
            println("Getting Client")
            var client = Socket(SERVER_ADDRESS, SERVER_PORT)     // The connection to server
            println("Connected to " + client)
            // Continuously check
            while (connected)
            {
                var reply = formatReply(data)
                var received_data = unpickler.load(client.getInputStream())
                //pickler.dump("From android", client.getOutputStream())    // Send back data
                var output = client.getOutputStream()
                output.write(pickler.dumps(reply))      // Send back data
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

    fun setAddress(addr : String)
    {
        SERVER_ADDRESS = addr
    }

    fun setPort(port: Int)
    {
        SERVER_PORT = port
    }
}