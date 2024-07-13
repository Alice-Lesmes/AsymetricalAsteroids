package com.example.asymetricasteroids

import android.app.AlertDialog
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.asymetricasteroids.ui.theme.AsymetricAsteroidsTheme
import com.ziclix.python.sql.WarningEvent
import net.razorvine.pickle.Pickler
import net.razorvine.pickle.Unpickler
import org.python.antlr.op.Mod
import java.io.FileInputStream
import java.io.IOException
import java.io.InputStream
import java.net.Socket


object Test {
    @Throws(IOException::class)
    @JvmStatic
    fun main(args: Array<String>) {
        val filename = args[0]
        val inputStream: InputStream = FileInputStream(filename)
        val unpickler = Unpickler()
        val pickler = Pickler()

        val data = unpickler.load(inputStream) as Map<String, Any>
    }
}
// SOcket stuff




/*fun server() {
    val server = ServerSocket(8000)
    val client = server.accept()
    val output = PrintWriter(client.getOutputStream(), true)
    val input = BufferedReader(InputStreamReader(client.inputStream))

    output.println("${input.readLine()} back")
}*/

// UI AND MAIN
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        /*var client = Client(InetAddress.getByName("192.168.122.1"))
        Thread({
            var client = Client("192.168.122.1")
            client.socket.connect()
        })*/

        enableEdgeToEdge()
        setContent {
            AsymetricAsteroidsTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    Alert()
                    ModuleView()
                    /*Button(onClick = { println("ALIVE?: " + client.isAlive()) }) {
                        Text(text = "IS ALIVE?")*/

                    //}

                }
            }
        }
    }
}

fun connect(addr : String, port: Int) {
    val connected = true
    println("Getting Client")
    var client = Socket(addr, port)     // The connection to server
    println("Connected to " + client)
    while (connected)
    {

        var reply = "Hello"
        val pickler = Pickler()     // Allows to pickle data
        val unpickler = Unpickler()     // Allows to unpickle data
        val received_data = unpickler.load(client.getInputStream())
        client.outputStream.write(pickler.dumps(reply))     // Send back data
        println("Receiving: " + unpickler.load(client.getInputStream()))

        if (received_data.toString() == "")
        {
            client.close()
            break
        }
    }
}


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun Alert() {
    var showAlert by remember {
        mutableStateOf(true)
    }
    if (showAlert)
    {
        AlertDialog(
            onDismissRequest = { showAlert = false },
            title = { Text("Welcome to the Automated Crew System!",
                fontWeight = FontWeight.ExtraBold) },
            text = { greetingAlertText() },
            confirmButton = {
                Button(onClick = { showAlert = false;
                    Thread({connect(addr = "192.168.0.222", 8000)}).start() }) {
                    Text(text = "Good luck...")
                }
            }
        )
    }

}

@Composable
fun greetingAlertText()
{
    Column {
        Text(text = "No longer a need for manual oversight",
            fontWeight = FontWeight.Light)
        Row(modifier = Modifier.padding(top=10.dp, bottom= 10.dp)) {
            Icon(imageVector = Icons.Filled.Warning, contentDescription = null, tint = Color.Red,
                )
            Text(text = "CRITICAL DAMAGE SUSTAINED TO: [AUTOMATED CREW SYSTEM]",
                fontWeight = FontWeight.Bold, color = Color.Yellow
            )
            Icon(imageVector = Icons.Filled.Warning, contentDescription = null, tint = Color.Red,
                )

        }
        Text(text = "Manual resource allocation required\n")

        Text(fontWeight = FontWeight.SemiBold, text = "Warning: Applying more power to a module than available may cause overcharge damage to the module requiring a restart")
        Text("\nTo manually reset ship module:\n\t1. Ensure [2] power is not in use\n\t2. Tap module name")
    }
}

@Composable
fun MainView()
{

}

@Composable
fun ModuleView()
{
    // Class of data, so can just grab stuff using methods -\_(<.<)_/-
    var data = Data()
    data.printAllData()
    Column(modifier = Modifier
        .padding(20.dp)) {
        PowerText(data.getAvailablePower())
        // Class of module
        var O2 = Module("O2", 2, data)
        var radar = Module("Radar", 2, data)
        var engines = Module("Engines", 2, data)
        // The actual UI
        O2.statefulModule()
        radar.statefulModule()
        engines.statefulModule()

        ElementSelect(data)
        Button(onClick = { data.printAllData() }) {
            
        }
    }
}
@Composable
fun PowerText(total_power: Int)
{
    Text(text = "Total Power: " + total_power,
        fontSize = 40.sp,
        fontWeight = FontWeight.Bold,
        textAlign = TextAlign.Center,
        modifier = Modifier.padding(20.dp)
    )
}

@Composable
fun ElementSelect(data: Data)
{
    var CurrentWeapon by remember { mutableStateOf("Standard") }
    Row {
        statefulElementalWeapon(name = "Standard", current_weapon = CurrentWeapon, data = data)
        statefulElementalWeapon(name = "Element 1", current_weapon = CurrentWeapon, data = data)
        statefulElementalWeapon(name = "Element 2", current_weapon = CurrentWeapon, data = data)

    }

}

@Composable
fun statefulElementalWeapon(name: String, current_weapon: String, data: Data)
{
    var CurrentWeapon by remember { mutableStateOf("Standard") }
    ElementalWeapon(name = name, enabled = CurrentWeapon == name,
        onButtonPress = {data.updateElement(name); CurrentWeapon = data.getWeaponElement()})
}

@Composable
fun ElementalWeapon(name: String, enabled: Boolean, onButtonPress: () -> Unit)
{
    Button(onClick = { onButtonPress()}, modifier = Modifier.padding(15.dp)) {
        Text(text = name,
            fontWeight = if (enabled) FontWeight.Bold else FontWeight.Light
        )

    }
}

/*

@Composable
fun Module(name: String, max_power: Int)
{

    var current_power by sending_data[name]
    var current_power_text by remember {
        mutableStateOf("")
    }
    Row(modifier = Modifier.padding(20.dp), horizontalArrangement = Arrangement.SpaceEvenly) {

        Button(onClick = {
                sending_data[name]
             }
            , enabled = if (current_power == 0) false else true)
            {
                Icon(
                    imageVector = Icons.Filled.KeyboardArrowDown,
                    contentDescription = null,
                )
            }
        Column(modifier = Modifier
            .padding(10.dp)) {
            Text(
                text = name,
                fontSize = 30.sp,
                fontWeight = FontWeight.ExtraBold,
                color = if (current_power == 0) Color.Red else Color.White
            )
            Text(
                text = if (current_power== 0)"" else "Power: " + current_power.toString()
            )
        }

        Button(onClick = {current_power++ }, enabled = if (current_power < max_power) true else false)
        {
            Icon(
                imageVector = Icons.Filled.KeyboardArrowUp,
                contentDescription = null,
                )
        }
    }
}
*/

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    AsymetricAsteroidsTheme {

    }
}