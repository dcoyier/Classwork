// Author: Dashiell Coyier
// Starter code from Carleton College CS 201 f25, taught by Anya Vostinar


import kotlin.collections.emptyList
import java.io.File

class IMDBGraph {

    /***************** Constructor (plus helper method) *****************/

    // Our graph is represented by a pair of maps
    val performersToMovies = HashMap<String, MutableList<String>>()
    val moviesToPerformers = HashMap<String, MutableList<String>>()

    // These two maps just connect performer ID to name and movie ID to name; it
    // might make playing around with the data more pleasant to have access to them
    val movieIdsToTitles = HashMap<String, String>()
    val performerIdsToNames = HashMap<String, String>()

    // In the constructor, read in all of the data from the .tsv files
    init {
        // Read in performer IDs and names
        var reader = File("src/main/resources/performer-names.tsv").bufferedReader()
        while (reader.ready()) {
            val (nameid, name) = reader.readLine().split("\t")
            performerIdsToNames[nameid] = name
        }
        reader.close()

        // Read in titles
        println("Reading titles")
        reader = File("src/main/resources/movie-titles.tsv").bufferedReader()
        while (reader.ready()) {
            val (titleid, title) = reader.readLine().split("\t")
            movieIdsToTitles[titleid] = title
        }
        reader.close()

        // Read in actual performances (a performer appearing in a movie)
        reader = File("src/main/resources/performances.tsv").bufferedReader()
        while (reader.ready()) {
            val (titleid, nameid) = reader.readLine().split("\t")
            addEntry(nameid, titleid)
        }
        reader.close()
    }

    /* This function adds a performer ID and a movie title ID to both maps. */
    fun addEntry(performerId: String, movieId: String) {
        var titles = performersToMovies[performerId]
        if (titles == null) {
            titles = mutableListOf<String>()
            performersToMovies[performerId] = titles
        }
        titles.add(movieId)

        var names = moviesToPerformers[movieId]
        if (names == null) {
            names = mutableListOf()
            moviesToPerformers[movieId] = names
        }
        names.add(performerId)
    }
    
    /***************** Part A: Find connected performers *****************/

    /*
        connectedPerformers determines the performers within a certain number of steps of a given performer
        @params performerId, the performer to find the connected performers of
        @params maxDistance, the maximum amount of connections between the performerId and connected performers
        @return a set of strings of performers within maxDistance connection
     */
    fun connectedPerformers(performerId: String, maxDistance: Int): Set<String> {
        // initializing the colleagues mutable set to store the connected performers
        var colleagues = mutableSetOf<String>()
        var movies = performersToMovies.get(performerId)

        // first iteration, maxDistance >= 1
        if (movies != null) {
            for (movie in movies) {
                var performers = moviesToPerformers.get(movie)
                if (performers!= null) for (performer in performers) colleagues.add(performer)
            }
        }

        // iterate additional times if the maxDistance is greater
        for (i in 1..(maxDistance - 1)) {
            var newColleagues = mutableSetOf<String>()
            for (colleague in colleagues) {
                var movies = performersToMovies.get(colleague)
                if (movies != null) {
                    for (movie in movies) {
                        var performers = moviesToPerformers.get(movie)
                        if (performers!= null) for (performer in performers) newColleagues.add(performer)
                    }
                }
            }
            colleagues.addAll(newColleagues)
        }

        return colleagues.toSet()
    }
    
    /***************** Part B: Find a path between performers *****************/

    /* This data class represents a performer-movie pair. */
    data class Connection(val performerId: String, val movieId: String)

    /* This function returns a list of connections from the startPerformer to
       the endPerformer.

       If this function were called with nm0000197 and nm0647634, the return value
       could be this list of Connections:
       [Connection(nm0000197, tt0082934), Connection(nm0001448, tt0409379)]

       If there is no connection between the two, an empty list is returned.
     */
    fun shortestPath(startPerformer: String, endPerformer: String): List<Connection> {
        // initializing variables to aid in traversal and store information
        var startNode = startPerformer
        var queue = ArrayDeque<String>()
        val visitedAndConnection = HashMap<String, String>() // used to store path back to startPerformer
                                                             // key is movie/performer and value is connection to previous
        var neighbors: List<String>?

        // adding startNode to queue and visited
        queue.add(startNode)
        visitedAndConnection.put(startNode, startNode) // startNode has no previous

        // breadth first traversal
        while (!queue.isEmpty()) {
            var currentNode = queue.removeFirst()

            // currentNode can be a performer or a movie
            if (currentNode in performersToMovies.keys) {
                neighbors = performersToMovies.get(currentNode)
            } else {
                neighbors = moviesToPerformers.get(currentNode)
            }

            if (neighbors != null) {
                // iterating through neighbors, adding neighbors to visited and to queue
                for (neighbor in neighbors) {
                    if (neighbor !in visitedAndConnection.keys) {
                        visitedAndConnection.put(neighbor, currentNode)
                        queue.add(neighbor)
                        if (neighbor == endPerformer) {
                            break
                        }
                    }
                }
            }
        }

        // initializing variables for finding shortestPath (path from endPerformer to StartPerformer)
        val path = mutableListOf<Connection>()
        var previous = endPerformer
        var nextMovie = visitedAndConnection[previous]
        var nextPerformer = visitedAndConnection[nextMovie]

        // backtracking to start after breadth first traversal is complete
        while (true) {
            if (nextPerformer == null || nextMovie == null) {
                // return empty list if there is no connection
                return listOf<Connection>()
            }

            // adding connection to start of the path list
            path.add(0, Connection(nextPerformer.toString(), nextMovie.toString()))

            // adjusting variables for next iteration
            previous = nextPerformer
            nextMovie = visitedAndConnection[previous] 
            nextPerformer = visitedAndConnection[nextMovie]

            if (previous == startPerformer) {
                break
            }
        }

        return path.toList()
    }
}
