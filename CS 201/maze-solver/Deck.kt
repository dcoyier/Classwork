// Author: Dashiell Coyier
// Source code from CS 201 f25, taught by Anya Vostinar


class Deck(initialCardOrdering: String) {

    var cards: Node? = null
    var numCards = 0

    init {
        val cardNumberList = initialCardOrdering.split(' ')
        if (cardNumberList.isEmpty()) {
            throw Exception("Deck empty.")
        }

        numCards = cardNumberList.size
        lateinit var current: Node
        for (cardString in cardNumberList) {
            val cardValue = cardString.toInt()
            if (cards == null) {
                // First node, special case
                val firstNode = Node(cardValue, null, null)
                cards = firstNode
                current = firstNode
            } else {
                // Any other node
                val card = Node(cardValue, current, null)
                current.next = card
                current = card
            }
        }

        // Wrap last card around
        current.next = cards
        cards!!.previous = current
    }

    /*
     * The getString() function returns a string of space (" ") delimited values of the cards
     * @params n specifies the amount of values within the string. If n is greater than the amount of unique cards, the deck loops back through cyclically
     * @return the string configuration of the cards
     */
    fun getString(n: Int): String {
        var returnStr = ""

        var current = cards
        var count = 0

        // moving n spots down the deck
        while (count < n) {
            returnStr = returnStr + current!!.value + " "
            current = current!!.next
            count++
        }

        // removes the final space character and returns the string
        return returnStr.dropLast(1)
    }

    /*
     * The getStringBackwards() function returns a string of space (" ") delimited values of the cards in reverse order, starting at the final card in the deck
     * @params n specifies the amount of values within the string. If n is greater than the amount of unique cards, the deck loops back through cyclically
     * @return the string configuration of the cards
     */
    fun getStringBackwards(n: Int): String {
        var returnStr = ""

        var current = cards!!.previous
        var count = 0

        // moving n spots up the deck
        while (count < n) {
            returnStr = returnStr + current!!.value + " "
            current = current!!.previous
            count++
        }

        // removes the final space character and returns the string
        return returnStr.dropLast(1)
    }

    /*
     * The countDown() function returns the value "i" cards from the start where "i" is the value of the first card
     * @return the string configuration of the cards
     */
    fun countDown(): Int {
        var topValue = cards!!.value
        
        // if it's a joker, assume 27
        if (topValue == 28) {
            topValue = 27
        }

        var count = 0
        var current = cards

        while (count < topValue) {
            current = current!!.next
            count++
        }

        return current!!.value
    }

    /*
     * The swapJokerA() modifies the card ordering to swap the jokerA card, value 27, with its next card in the deck
     */
    fun swapJokerA() {
        // locating jokerA
        var current = cards
        while (current!!.value != 27) {
            current = current!!.next
        }

        // order is "previous" "jokerA" "next" "neighbor"
        val jokerA = current
        val previous = jokerA!!.previous
        val next = jokerA!!.next
        val neighbor = next!!.next

        // reconfiguring pointers for correct jokerA swap
        previous!!.next = next 
        next.previous = previous
        next.next = jokerA
        jokerA.previous = next
        jokerA.next = neighbor
        neighbor!!.previous = jokerA 

        // adjusting top of cards pointer
        if (jokerA == cards) {
            cards = next
        } else if (next == cards) {
            cards = jokerA
        }
    }

    /*
     * The swapJokerB() modifies the card ordering to swap the jokerB card, value 28, with the card two spots further in the deck
     */
    fun swapJokerB() {
        // locating jokerB
        var current = cards
        while (current!!.value != 28) {
            current = current!!.next
        }

        // order is "previous" "jokerB" "next" "afterNext" "neighbor"
        val jokerB = current
        val previous = jokerB!!.previous
        val next = jokerB!!.next
        val afterNext = next!!.next
        val neighbor = afterNext!!.next

        // reconfiguring pointers for correct jokerB swap
        previous!!.next = next 
        next.previous = previous
        afterNext.next = jokerB
        jokerB.previous = afterNext
        jokerB.next = neighbor
        neighbor!!.previous = jokerB 

        // adjusting top of cards pointer
        if (jokerB == cards) {
            cards = next
        } else if (next == cards) {
            cards = afterNext
        } else if (afterNext == cards) {
            cards = jokerB
        }
    }

    /*
     * The tripleCut() modifies the card ordering to swap all cards before the first joker (value of 27 or 28) with all cards after the second joker
     */
    fun tripleCut() {
        // locating first joker
        var current = cards
        while(true) {
            if (current!!.value == 27 || current!!.value == 28) {
                break
            }
            current = current!!.next
        }
        val firstJoker = current
        current = firstJoker!!.next

        // locating second joker
        while(true) {
            if (current!!.value == 27 || current!!.value == 28) {
                break
            }
            current = current!!.next
        }
        val secondJoker = current

        // assigning variables whose pointers will change
        val set1Start = cards
        val set1End = firstJoker!!.previous
        val set2Start = secondJoker!!.next
        val set2End = cards!!.previous

        // handling edge cases
        if (firstJoker == cards) {
            cards = set2Start 
            return           
        } else if (secondJoker == cards!!.previous) {
            cards = firstJoker
            return
        }

        // reconfiguring pointers to triple cut deck
        set2Start!!.previous = set1End
        set2End!!.next = firstJoker
        firstJoker.previous = set2End
        secondJoker.next = set1Start
        set1Start!!.previous = secondJoker
        set1End!!.next = set2Start
        cards = set2Start
    }
}
