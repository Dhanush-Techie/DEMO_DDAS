package main

import (
	"fmt"
	"hash"
	"io"
	"log"
	"net/http"

	"golang.org/x/crypto/blake2b"
)

// Function to create a new BLAKE2b-256 hash object
func newHash() hash.Hash {
	hashObj, err := blake2b.New256(nil)
	if err != nil {
		log.Fatal(err)
	}
	return hashObj
}

func main() {
	// Handle POST requests to receive chunks
	http.HandleFunc("/upload", chunkHandler)

	fmt.Println("Server started at :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

// chunkHandler receives the entire file (assuming chunks are sent in one request), updates the hash, and responds
func chunkHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, "Only POST is allowed", http.StatusMethodNotAllowed)
		return
	}

	// Create a new hash object for each new upload (reset the hash for each file)
	hashObj := newHash()

	// Read the entire file data and update the hash object
	_, err := io.Copy(hashObj, r.Body)
	if err != nil {
		http.Error(w, "Failed to read file", http.StatusInternalServerError)
		return
	}

	// Calculate the final hash value for the file
	finalHash := fmt.Sprintf("%x", hashObj.Sum(nil))
	fmt.Println("File received and hashed. Final hash value:", finalHash)

	// Respond with the hash value
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(finalHash))
}
