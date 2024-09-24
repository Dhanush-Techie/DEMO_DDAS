package main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/fsnotify/fsnotify"
	"golang.org/x/sys/windows"
	"os/user"
	"syscall"
)

// Helper function to check if the path is within excluded folders
func shouldIgnore(path string, excludeFolders []string) bool {
	for _, folder := range excludeFolders {
		if strings.HasPrefix(strings.ToLower(path), strings.ToLower(folder)) {
			return true
		}
	}
	return false
}

// Event handler for file system events
func handleEvent(event fsnotify.Event, excludeFolders []string) {
	if shouldIgnore(event.Name, excludeFolders) {
		return
	}

	switch event.Op {
	case fsnotify.Create:
		fmt.Printf("File created: %s\n", event.Name)
	case fsnotify.Write:
		fmt.Printf("File modified: %s\n", event.Name)
	case fsnotify.Remove:
		fmt.Printf("File deleted: %s\n", event.Name)
	}
}

// Function to monitor a folder
func monitorFolder(watcher *fsnotify.Watcher, folderPath string, excludeFolders []string) error {
	err := filepath.Walk(folderPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.IsDir() {
			if shouldIgnore(path, excludeFolders) {
				return filepath.SkipDir
			}
			err = watcher.Add(path)
			if err != nil {
				return err
			}
		}
		return nil
	})
	return err
}

// Function to get available drives
func getAvailableDrives() ([]string, error) {
	drives := []string{}
	buffer := make([]byte, syscall.MAX_PATH)

	driveMask, err := windows.GetLogicalDrives()
	if err != nil {
		return nil, err
	}

	for i := 0; i < 26; i++ {
		if driveMask&(1<<uint(i)) != 0 {
			drive := fmt.Sprintf("%c:\\", 'A'+i)
			_, err := windows.GetVolumeInformation(syscall.StringToUTF16Ptr(drive), buffer, syscall.MAX_PATH, nil, nil, nil, buffer, syscall.MAX_PATH)
			if err == nil {
				drives = append(drives, drive)
			}
		}
	}
	return drives, nil
}

func main() {
	// Get current username
	currentUser, err := user.Current()
	if err != nil {
		log.Fatal(err)
	}
	username := currentUser.Username

	// Exclude the Temp folder: C:\Users\{username}\AppData\Local\Temp
	excludeFolder := filepath.Join("C:", "Users", username, "AppData", "Local", "Temp")
	fmt.Printf("Monitoring C:\\Users folder, excluding %s\n", excludeFolder)

	// Create a new file system watcher
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		log.Fatal(err)
	}
	defer watcher.Close()

	// List of excluded folders
	excludeFolders := []string{excludeFolder}

	// Monitor the C:\Users folder
	usersFolder := filepath.Join("C:", "Users")
	err = monitorFolder(watcher, usersFolder, excludeFolders)
	if err != nil {
		log.Fatal(err)
	}

	// Get remaining drives
	drives, err := getAvailableDrives()
	if err != nil {
		log.Fatal(err)
	}

	// Exclude C: since we're already monitoring C:\Users
	for _, drive := range drives {
		if drive != "C:\\" {
			fmt.Printf("Starting observer for drive: %s\n", drive)
			err = monitorFolder(watcher, drive, excludeFolders)
			if err != nil {
				log.Fatal(err)
			}
		}
	}

	// Event loop
	done := make(chan bool)
	go func() {
		for {
			select {
			case event, ok := <-watcher.Events:
				if !ok {
					return
				}
				handleEvent(event, excludeFolders)
			case err, ok := <-watcher.Errors:
				if !ok {
					return
				}
				fmt.Printf("Error: %v\n", err)
			}
		}
	}()

	// Keep the program running
	<-done
}
