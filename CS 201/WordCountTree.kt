// Author: Dashiell Coyier
// Starter code from Carleton College CS 201 f25, taught by Anya Vostinar


/**
 * WordCountTree class contains word counts within a provided series of strings.
 * Each node of the WordCountTree (WCT) contains a count. The children of a node
 * are all of the characters that could come after the node's character to
 * represent a word.
 */
class WordCountTree {
    // Nobody else needs to see how we internally store nodes, so
    // we keep the data class private
    private data class Node(
        var count: Int = 0,
        val children: MutableMap<Char, Node> = mutableMapOf<Char, Node>())

    // Store a pointer to the root node in the tree
    private var root: Node = Node()

    /**
     * Returns a string representation of the tree.
     */
    override fun toString(): String {
        return root.toString()
    }

    /**
     * Adds 1 to the existing count for given word, 
     * or adds given word to the WordCountTree with a count of 1 
     * if it is not already present.
     * Implementation must be recursive, not iterative.
     */
    fun incrementCount(word: String) {
        incrementCountRecur(word)
    }
    
    /**
     * Contains all of the code for incrementCount, but moved to a different
     * function to have parameter of newCur (type Node?) and default
     * setting for root (these are private)
     */
    private fun incrementCountRecur(word: String, newCur: Node? = root) {
        var current = newCur

        // if node already exists
        if (current?.children[word[0]] != null) {
            current = current!!.children[word[0]]

            // if at end of word
            if (word.length == 1) {
                current!!.count += 1
                return
            }

            incrementCountRecur(word.substring(1, word.length), current)
        } 
        
        // if need to add node
        else {
            var newNode = Node()
            current!!.children[word[0]] = newNode
            current = newNode

            // if at end of word
            if (word.length == 1) {
                newNode.count += 1
                var count = current!!.children
                return
            }

            incrementCountRecur(word.substring(1, word.length), current)
        }
    }

    /**
     * Returns the count of word. Returns 0 if word is not present.
     * Implementation must be recursive, not iterative.
     */
    fun getCount(word: String): Int {
        return getCountRecur(word)
    }

    /**
     * Contains all of the code for getCount, but moved to a different
     * function to have parameter of current (type Node?) and default
     * setting for root (these are private)
     */
    private fun getCountRecur(word: String, current: Node? = root): Int {
        if (current?.children[word[0]] == null) return 0
        if (word.length == 1) return current!!.children[word[0]]!!.count
        return getCountRecur(word.substring(1, word.length), current!!.children[word[0]])
    }

    /**
     * Returns true if word is stored in this WordCountTree
     * with a count greater than 0, and false otherwise.
     * Implementation must be recursive, not iterative.
     */
    fun contains(word: String): Boolean {
        return getCount(word) > 0
    }

    /**
     * Returns a MutableMap of all words in WordCountTree that
     * start with the given prefix, mapped to their counts.
     * If prefix is not present, returns an empty MutableMap.
     */
    fun getAutocompletionMap(prefix: String): MutableMap<String, Int> {
        var current: Node? = root

        // moving to the start position
        for (char in prefix) {
            current = current!!.children[char]
        }

        // calling the recursive function to retrieve map
        return getMapRecur(prefix, current)
    }

    /**
     * Used in the getAutocompleteMap function and recursively
     * formulates a map that contains all strings, counts that include
     * the prefix.
     */
    private fun getMapRecur(newPrefix: String, newCur: Node?): MutableMap<String, Int> {
        var current = newCur
        var prefix = newPrefix
        var newMap = mutableMapOf<String, Int>()

        // iterating through and adding within this level and values to newMap
        for ((key, value) in current!!.children) {
            if (value!!.count> 0) newMap[prefix + key] = value!!.count
        }

        // calling getAutoComplete on all nodes in all levels
        for ((key, value) in current!!.children) {
            newMap += getMapRecur(prefix + key, value).toMap()
        }
        
        return newMap
    }
}
