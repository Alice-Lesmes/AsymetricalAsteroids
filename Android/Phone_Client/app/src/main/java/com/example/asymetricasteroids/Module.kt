package com.example.asymetricasteroids

import android.annotation.SuppressLint
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.filled.KeyboardArrowUp
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
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
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

class Module(val module: String, val max: Int, data: Data)
{
    val name : String = module
    val max_power = max
    var current_power : Int = 0
    var trial = data
    /*val available_power = data.getAvailablePower()
    var forward_data = data*/


    @Composable
    fun statefulModule()
    {
        var current_power by remember {
            mutableStateOf(0)
        }
        var available_power = trial.getAvailablePower()

        statelessModule(onIncrement = { current_power++}, onDecrement = { current_power--},
            tapText = {if (trial.getPower(module) == 0 && trial.getAvailablePower() >= max)
            {
                current_power = max
                available_power = trial.getAvailablePower()
            }
            else if (trial.getPower(module) == 1)
            {
                current_power = 0
                available_power = trial.getAvailablePower()
            }
            else if (trial.getPower(module) == max)
            {
                  current_power = 0
                available_power = trial.getAvailablePower()
              }},
            current_power = current_power,
            available_power = available_power)
        trial.updatePower(module, current_power)
        trial.printAllData()
    }

    @SuppressLint("NotConstructor")
    @Composable
    fun statelessModule(onIncrement: () -> Unit, onDecrement: () -> Unit, tapText: () -> Unit,
                        current_power: Int,
                        available_power: Int)
    {
        Row(modifier = Modifier.padding(top= 10.dp).fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly)
        {
            Button(onClick = {
                onDecrement();
            }, enabled = if (current_power == 0) false else true,
                modifier = Modifier.weight(1f))
            {
                Icon(
                    imageVector = Icons.Filled.KeyboardArrowDown,
                    contentDescription = null,
                )
            }
            Column(modifier = Modifier.weight(2f)
                .padding(10.dp)) {
                Text(
                    text = name,
                    fontSize = 30.sp,
                    textAlign = TextAlign.Center,

                    fontWeight = FontWeight.ExtraBold,
                    color = if (current_power == 0) Color.Red else Color.White,
                    modifier = Modifier.clickable { tapText() }
                )
                Text(
                    text = if (current_power== 0)"" else "Power: " + current_power.toString()
                )
            }

            Button(onClick =
            {
                onIncrement();},
                enabled = if (current_power < max_power && available_power > 0) true else false,
                modifier = Modifier.weight(1f))
            {
                Icon(
                    imageVector = Icons.Filled.KeyboardArrowUp,
                    contentDescription = null,
                )
            }
        }
    }
}