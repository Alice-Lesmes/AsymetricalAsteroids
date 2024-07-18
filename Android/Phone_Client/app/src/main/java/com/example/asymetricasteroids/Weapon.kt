package com.example.asymetricasteroids

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue

class WeaponChoice() {
    var chosen_element = "Laser"
    @Composable
    fun WeaponToggle()
    {
        var checked by remember { mutableStateOf(true) }
        Row {
            Column {
                Text(text = "Laser")
                Switch(checked = checked, onCheckedChange = {checked = it})
            }
        }
    }
}

class Weapon(name: String)
{
    @Composable
    fun WeaponToggle()
    {
        var checked by remember { mutableStateOf(true) }
        Row {
            Column {
                Text(text = "Laser")
                Switch(checked = checked, onCheckedChange = {checked = it})
            }
        }
    }
}