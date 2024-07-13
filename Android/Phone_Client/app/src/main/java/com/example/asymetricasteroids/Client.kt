package com.example.asymetricasteroids

import android.os.Handler
import android.os.Looper
import android.util.Log
import java.io.IOException
import java.io.InputStream
import java.io.OutputStream
import java.net.InetAddress
import java.net.InetSocketAddress
import java.net.Socket
import java.util.concurrent.Executors

class Client(hostAddress: InetAddress): Thread() {

    var hostAddress: String = hostAddress.hostAddress
    lateinit var inputStream: InputStream
    lateinit var outputStream: OutputStream
    lateinit var socket: Socket

    fun write(byteArray: ByteArray){
        try {
            outputStream.write(byteArray)
        }catch (ex: IOException){
            ex.printStackTrace()
        }
    }

    override fun run() {
        try {
            socket = Socket()
            socket.connect(InetSocketAddress(hostAddress,8000),500)
            inputStream = socket.getInputStream()
            outputStream = socket.getOutputStream()
        }catch (ex: IOException){
            ex.printStackTrace()
        }
        val executor = Executors.newSingleThreadExecutor()
        var handler = Handler(Looper.getMainLooper())

        executor.execute(kotlinx.coroutines.Runnable {
            kotlin.run {
                val buffer =ByteArray(1024)
                var byte:Int
                while (true){
                    try{
                        byte = inputStream.read(buffer)
                        if(byte>0){
                            val finalBytes = byte
                            handler.post(Runnable{
                                kotlin.run {
                                    val tmpMeassage = String(buffer,0,finalBytes)

                                    Log.i("client class", tmpMeassage)
                                }
                            })
                        }
                    }catch (ex: IOException){
                        ex.printStackTrace()
                    }
                }
            }
        })
    }

}