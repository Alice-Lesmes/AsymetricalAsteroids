package com.example.asymetricasteroids

class Data {
    // This is hard-coded <- BAD!
    var o2 = 0
    var engines = 0
    var radar = 0
    var element = "Standard"
    val total_power = 4

    fun getAvailablePower(): Int
    {
        var available_power = total_power - o2 - engines - radar - weaponPower()
        return available_power
    }
    fun updatePower(name: String, input: Int)
    {
        // This is really bad but i don't have time to think -\_(-_-)_/-
        // Essentially a switch case
        when (name)
        {
            "O2" -> o2 = input
            "Engines" -> engines = input
            "Radar" -> radar = input
        }
    }
    fun getPower(name: String): Int {
        // Returns the relevant data
        var result = when (name)
        {
            "O2" -> o2
            "Engines" -> engines
            "Radar" -> radar
            else -> 0
        }
        return result
    }
    fun printAllData()
    {
        println(o2)
        println(engines)
        println(radar)
        println(element)
    }
    fun getWeaponElement(): String
    {
        return element
    }
    fun updateElement(input_element: String)
    {
        element = input_element
    }
    fun weaponPower(): Int
    {
        // Returns the power drawn by the weapon (effected by element)
        if (element == "Standard") return 0
        else return 1
    }
}