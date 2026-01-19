// Author: Dashiell Coyier
// Starter code from Carleton College CS 201 f25, taught by Anya Vostinar


import kotlin.math.abs
import kotlin.random.Random

class CuckooHashMap<K, V>(tableSize: Int) : CuckooSetup<K, V>(tableSize) {

    // Look up a key, and get the corresponding value. Try both tables as
    // needed. Returns null if not found.
    fun get(key: K): V? {
        if (lookUpKey(0, key) == key) {
            return lookUpValue(0, key)
        } else if (lookUpKey(1, key) == key) {
            return lookUpValue(1, key)
        } else {
            return null
        }
    }

    // Adds a key and a value to one of the hash tables.
    fun set(key: K, value: V) {
        val updatedRecursively = addOrUpdateRecur(key, value)

        if (updatedRecursively != null) {
            rehashUntilSuccess(updatedRecursively)
        }
    }

    // HELPER FUNCTIONS
    private fun lookUpKey(tableNum: Int, key: K): K? = tables[tableNum][cuckooHashCode(tableNum, key) % tableSize]?.key

    private fun lookUpValue(tableNum: Int, key: K): V? =
        tables[tableNum][cuckooHashCode(tableNum, key) % tableSize]?.value

    fun moddedHash(tableNum: Int, key: K): Int = cuckooHashCode(tableNum, key) % tableSize

    private fun addOrUpdate(key: K, value: V): Entry<K, V>? {
        if (lookUpValue(0, key) == null) {
            tables[0][moddedHash(0, key)] = Entry(key, value)
            return null
        } else {
            val temp = tables[0][moddedHash(0, key)]
            tables[0][moddedHash(0, key)] = Entry(key, value)

            val table2Spot: Entry<K, V>? = tables[1][moddedHash(1, temp!!.key)]
            tables[1][moddedHash(1, temp!!.key)] = temp

            return table2Spot
        }
    }

    private fun addOrUpdateRecur(key: K, value: V, count: Int = 0): Entry<K, V>? {
        var output: Entry<K, V>? = addOrUpdate(key, value)

        if (output == null) return null

        val newKey = output!!.key
        val newValue = output!!.value
        val newCount = count + 1

        if (count > MAX_LOOP) return Entry(newKey, newValue)

        return addOrUpdateRecur(newKey, newValue, newCount)
    }

    private fun rehashUntilSuccess(lastValue: Entry<K, V>?) {
        val allEntries: Array<Entry<K, V>?> = arrayOfNulls(tableSize * 2 + 1)
        var curIndex = 0

        for (entry in tables[0]) {
            // println(entry?.value)
            allEntries[curIndex] = entry
            curIndex++
        }

        for (entry in tables[1]) {
            // println(entry?.value)
            allEntries[curIndex] = entry
            curIndex++
        }

        // adding final entry
        allEntries[curIndex] = lastValue

        while (true) {
            seed++
            tableSize *= 2
            if (rehash(allEntries)) {
                break
            }
        }
    }

    private fun rehash(allEntries: Array<Entry<K, V>?>): Boolean {
        val newTables = listOf(Array<Entry<K, V>?>(tableSize) { null }, Array<Entry<K, V>?>(tableSize) { null })
        tables = newTables

        for (entry in allEntries) {
            if (entry != null) {
                val outputRecur = addOrUpdateRecur(entry!!.key, entry!!.value)
                if (outputRecur != null) {
                    return false
                }
            }
        }

        return true
    }

    fun getTheTableSize(): Int {
        return tableSize
    }
}
