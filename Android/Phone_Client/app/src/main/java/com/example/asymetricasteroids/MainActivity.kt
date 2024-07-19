package com.example.asymetricasteroids

import android.os.Bundle
import android.provider.Telephony.Carriers.PORT
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
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
import kotlinx.coroutines.*
import kotlinx.coroutines.Dispatchers
import org.jetbrains.annotations.Async
import kotlin.concurrent.thread

// UI AND MAIN *stuff*
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        /*var client = Client(InetAddress.getByName("192.168.122.1"))
        Thread({
            var client = Client("192.168.122.1")
            client.socket.connect()
        })*/
        val SERVER_ADDRESS = "192.168.0.12"
        val PORT = 8000
        var dataManager = Data()
        thread {
            var client = Client(SERVER_ADDRESS, PORT, dataManager)
            runBlocking { client.connect() }

        }
        enableEdgeToEdge()
        setContent {
            AsymetricAsteroidsTheme {
                // The data that all the code draws from

                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    mainView(dataManager)
                    /*Button(onClick = { println("ALIVE?: " + client.isAlive()) }) {
                        Text(text = "IS ALIVE?")*/

                    //}

                }
            }
        }
    }
}


@Composable
fun mainView(data: Data) {
    // The main view which holds the smaller views together and inits client connection

    var CriticalServerError by remember {
        mutableStateOf(false)
    }
    var showAlert by remember {
        mutableStateOf(true)
    }

    // Triggers on first launch and connects to server
    if (showAlert) Alert()
    // This would be used if there is no response from the server, but we don't care
    // Just hope for connection, if not, -\_(<: )_/-
    /*if (CriticalServerError)
    {
        AlertDialog(onDismissRequest = { CriticalServerError = false },
            title = { Text("Error connecting to server") },
            text = {
                Text(
                    "Check server is running and IP and PORT is correct\n" +
                            "IP: $SERVER_ADDRESS\nPORT: $PORT"
                )
            },
            confirmButton = {
                // System.exit should just quit the app
                Button(onClick = { showAlert = true}) {
                    Text(text = "Oh no... Reconnect!")
                }
            })
    }*/
    ModuleView(data)

    // Enable for debugging purposes only. Allows to print data sent to server
    Button(onClick = { println("Data get!"); data.printAllData() }) {
        Text(text = "Print DATa!S")
    }
}

@Composable
fun Alert() {
    var showAlert by remember {
        mutableStateOf(true)
    }

    if (showAlert) {
        AlertDialog(
            onDismissRequest = { showAlert = false },
            title = {
                Text(
                    "Welcome to the Automated Crew System!",
                    fontWeight = FontWeight.ExtraBold
                )
            },
            text = {
                // WOW! Lore! Let's go!
                greetingAlertText()
            },
            confirmButton = {
                Button(onClick = {
                    showAlert = false;

                })
                {
                    // This is the text of the button
                    Text(text = "Good luck...")
                }
            }
        )
    }

}

@Composable
fun greetingAlertText() {
    // OMG THIS IS SO MUCH LORE! LOOK AT IT! LOOK AT THE LORE! LOOOOORRRE!
    Column {
        Text(
            text = "No longer a need for manual oversight",
            fontWeight = FontWeight.Light
        )
        Row(modifier = Modifier.padding(top = 10.dp, bottom = 10.dp)) {
            Icon(
                imageVector = Icons.Filled.Warning, contentDescription = null, tint = Color.Red,
            )
            Text(
                text = "CRITICAL DAMAGE SUSTAINED TO: [AUTOMATED CREW SYSTEM]",
                fontWeight = FontWeight.Bold, color = Color.Yellow
            )
            Icon(
                imageVector = Icons.Filled.Warning, contentDescription = null, tint = Color.Red,
            )

        }
        Text(text = "Manual resource allocation required\n")

        Text(
            fontWeight = FontWeight.SemiBold,
            text = "Warning: Applying more power to a module than available may cause overcharge damage to the module requiring a restart"
        )
        Text("\nTo manually reset ship module:\n\t1. Ensure [2] power is not in use\n\t2. Tap module name")
    }
}

@Composable
fun ModuleView(data: Data) {
    // Class of data, so can just grab stuff using methods -\_(<.<)_/-
    var power_left by remember {
        mutableStateOf(data.getAvailablePower())
    }
    Column(
        modifier = Modifier
            .padding(20.dp)
    ) {
        // Class of module
        var O2 = Module("O2", 2, data)
        var radar = Module("Radar", 2, data)
        var engines = Module("Engines", 2, data)
        // The actual UI
        var o2Power by remember {
            mutableStateOf(0)
        }
        var enginesPower by remember {
            mutableStateOf(0)
        }
        var radarPower by remember {
            mutableStateOf(0)
        }
        var availablePower by remember {
            mutableStateOf(data.total_power)
        }
        PowerText(availablePower)
        O2.statelessModule(
            onIncrement = { o2Power++; availablePower-- },
            onDecrement = { o2Power--; availablePower++ },
            tapText = {
                // This is bad code, but whatever, it works
                if (o2Power == 0 && availablePower >= O2.max)
                    {
                        o2Power = O2.max
                        availablePower -= o2Power

                        data.updatePower(O2.name, o2Power)

                    }
                    else
                    {
                        availablePower += o2Power
                        o2Power = 0
                        data.updatePower(O2.name, o2Power)
                    }},
            available_power = availablePower,
            currentPower = o2Power
        )
        engines.statelessModule(
            onIncrement = { enginesPower++; availablePower--; data.updatePower(engines.name, enginesPower) },
            onDecrement = { enginesPower--; availablePower++; data.updatePower(engines.name, enginesPower) },
            tapText = {if (enginesPower == 0 && availablePower >= engines.max)
            {
                enginesPower = engines.max
                availablePower -= enginesPower

                data.updatePower(engines.name, enginesPower)

            }
            else
            {
                availablePower += enginesPower
                enginesPower = 0
            }},
            available_power = availablePower,
            currentPower = enginesPower
        )
        radar.statelessModule(
            onIncrement = { radarPower++; availablePower--; data.updatePower(radar.name, radarPower) },
            onDecrement = { radarPower--; availablePower++; data.updatePower(radar.name, radarPower) },
            tapText = {if (radarPower == 0 && availablePower >= radar.max)
            {
                radarPower = radar.max
                availablePower -= radarPower
                data.updatePower(radar.name, radarPower)

            }
            else
            {
                availablePower += radarPower
                radarPower = 0
            }},
            available_power = availablePower,
            currentPower = radarPower
        )

        ElementSelect(data)


    }
}



@Composable
fun PowerText(total_power: Int) {
    Text(
        text = "Total Power: " + total_power,
        fontSize = 40.sp,
        fontWeight = FontWeight.Bold,
        textAlign = TextAlign.Center,
        modifier = Modifier.padding(20.dp)
    )
}

@Composable
fun WeaponText(current_weapon: String) {
    Text(
        text = "Current Weapon: $current_weapon",
        fontWeight = FontWeight.Bold,
        fontSize = 30.sp,
        modifier = Modifier.padding(bottom = 5.dp)
    )
}

@Composable
fun ElementSelect(data: Data) {
    var CurrentWeapon by remember { mutableStateOf("Yellow") }

    Column {
        WeaponText(current_weapon = CurrentWeapon)

        Column(modifier = Modifier.fillMaxWidth()) {
            Row {
                for (weapon in arrayOf("Yellow", "Red"))
                    ElementalWeapon(
                        name = weapon,
                        onButtonPress = { CurrentWeapon = weapon;
                            data.updateElement(weapon) },
                        modifier = Modifier.weight(1f))
            }
            Row {
                for (weapon in arrayOf("Green", "Blue"))
                        ElementalWeapon(
                        name = weapon,
                        onButtonPress = { CurrentWeapon = weapon;
                            data.updateElement(weapon) },
                        modifier = Modifier.weight(1f))
            }


        }

    }

}

@Composable
fun ElementalWeapon(name: String, onButtonPress: () -> Unit, modifier: Modifier) {
    Button(
        onClick = { onButtonPress() },
        modifier = Modifier
            .padding(15.dp)
    ) {
        Text(text = name)

    }
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    AsymetricAsteroidsTheme {

    }
}