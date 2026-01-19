// Author: Dashiell Coyier
// Starter code from Carleton College CS 201 f25, taught by Anya Vostinar


/*
 * The LunarLander class contains properties of altitude, velocity, and fuel.
 * Its methods include burn(), which reduces fuel and modified altitude and velocity, and status(), which
 * returns whether the LunarLander has crashed, landed, or is still inflight.
 */

class LunarLander(var altitude: Int = 1000, var velocity: Int = 40, var fuel: Int = 25) {

    /*
     * The burn() burns fuel and changes the velocity and altitude of the LunarLander object accordingly
     * @param fuelRequested, the amount of fuel the user is hoping to burn, an Int value
     */
    fun burn(fuelRequested: Int) {
        var fuelBurned: Int

        // if there isn't enough fuel remaining, burn what is available instead
        if (fuelRequested > fuel) {
            fuelBurned = fuel
            fuel = 0
        } else {      // standard fuel burn (have enough)
            fuelBurned = fuelRequested
            fuel -= fuelBurned
        }

        // the change in velocity (meters/second) for each unit of fuel
        val METERS_PER_SECOND_PER_FUEL = 4

        // the effect of gravity on velocity (meters/second)
        val EFFECT_OF_GRAVITY = 2

        velocity -= METERS_PER_SECOND_PER_FUEL * fuelBurned      // impact of fuel used
        velocity += EFFECT_OF_GRAVITY       // adding the effect of gravity
        altitude -= velocity
    }

    /*
     * The status() returns the status of the LunarLander object. If it is at or below 0 altitude, it has crashed or landed,
     * depending on the velocity. Otherwise, it is inflight.
     * @return a String representing the state of the LunarLander ("inflight", "crashed", or "landed")
     */
    fun status(): String {
        when {
            altitude > 0 -> return "inflight"
            velocity >= 5 -> return "crashed"
            else -> return "landed"
        }
    }
}


fun main() {
    // welcome message
    println("Welcome to Lunar Lander!\n")
    var fuelToBurn: Int
    var quit: Boolean = false

    // determining player count
    print("Do you want to play with one or two players? Type '1' or '2': ")
    var playerCount: String? = readLine()   // it could be null
    if (playerCount != "1" && playerCount != "2") {
        print("\nIncorrect input. Please restart the program.")
    }

    // single player game
    if (playerCount == "1") {
        val myLunarLander = LunarLander()
        println("\nI hope you're ready to play! Enter -1 to exit the program.\n")
        while (myLunarLander.status() == "inflight") {
            println("Alt = ${myLunarLander.altitude} Vel = ${myLunarLander.velocity} Fuel = ${myLunarLander.fuel}")
            print("How much fuel to burn this round? ")

            // asking user to input how much fuel to burn
            var userInput: String? = readLine()
            fuelToBurn = userInput!!.toInt()

            // if -1 is entered, the program quits
            if (fuelToBurn == -1) {
                quit = true
                println("\nQuitting...")
                break
            }

            myLunarLander.burn(fuelToBurn)
        }

        // determining reason for end of game, either a crash or successful landing (only if game was not terminated by user)
        if (!quit) {
            println("Alt = ${myLunarLander.altitude} Vel = ${myLunarLander.velocity} Fuel = ${myLunarLander.fuel}\n")
            if (myLunarLander.velocity > 4) {
                println("Oh no, you crashed.")
            } else {
                println("Congratulations, you landed successfully!")
            }
        }
    }

    // two player game
    else if (playerCount == "2") {
        var turn = 1
        println("\nI hope you're ready to play! Enter -1 to exit the program.")
        val myLunarLander1 = LunarLander()
        val myLunarLander2 = LunarLander()

        while (myLunarLander1.status() == "inflight" && myLunarLander2.status() == "inflight") {
            if (turn == 1) {
                println("\nIt's player one's turn! Here is their status: ")
                println("Alt = ${myLunarLander1.altitude} Vel = ${myLunarLander1.velocity} Fuel = ${myLunarLander1.fuel}")
                print("How much fuel to burn this round? ")

                // asking user to input how much fuel to burn
                var userInput: String? = readLine()
                fuelToBurn = userInput!!.toInt()

                // if -1 is entered, the program quits
                if (fuelToBurn == -1) {
                    quit = true
                    println("\nQuitting...")
                    break
                }

                myLunarLander1.burn(fuelToBurn)

                // switching to next player's turn
                turn += 1
            } else if (turn == 2) {
                println("\nIt's player two's turn! Here is their status: ")
                println("Alt = ${myLunarLander2.altitude} Vel = ${myLunarLander2.velocity} Fuel = ${myLunarLander2.fuel}")
                print("How much fuel to burn this round? ")

                // asking user to input how much fuel to burn
                var userInput: String? = readLine()
                fuelToBurn = userInput!!.toInt()

                // if -1 is entered, the program quits
                if (fuelToBurn == -1) {
                    quit = true
                    println("\nQuitting...")
                    break
                }

                myLunarLander2.burn(fuelToBurn)

                // switching to next player's turn
                turn -= 1
            }
        }

        if (!quit) {
            // determining reason for end of game and congratulating winning player (only if game was not terminated by user)
            println("\nGame over. \nFinal status player one: Alt = ${myLunarLander1.altitude} Vel = ${myLunarLander1.velocity} Fuel = ${myLunarLander1.fuel}\nFinal status player two: Alt = ${myLunarLander2.altitude} Vel = ${myLunarLander2.velocity} Fuel = ${myLunarLander2.fuel}")
            if (myLunarLander2.status() == "crashed" || myLunarLander1.status() == "landed") {
                println("\nPlayer one wins!")
            } else {
                println("\nPlayer two wins!")
            }
        }

    }
}
