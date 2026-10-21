# Before / after

Examples of typical AI code and what a human developer does with it. Treat them as an illustration of the principle, not a template to copy.

## Python: loading a config

Before:

```python
# ============================================
# Configuration Loading Module
# ============================================

import json
import os
from typing import Dict, Any, Optional


def load_configuration_file(configuration_file_path: str) -> Optional[Dict[str, Any]]:
    """
    Load configuration from a JSON file.

    Args:
        configuration_file_path (str): The path to the configuration file.

    Returns:
        Optional[Dict[str, Any]]: The loaded configuration dictionary, or None if an error occurred.
    """
    # Check if the file exists
    if not os.path.exists(configuration_file_path):
        print(f"❌ Error: Configuration file not found at {configuration_file_path}")
        return None

    try:
        # Open and read the file
        with open(configuration_file_path, "r") as config_file:
            configuration_data: Dict[str, Any] = json.load(config_file)
        print("✅ Configuration loaded successfully!")
        return configuration_data
    except Exception as e:
        print(f"❌ An error occurred while loading the configuration: {e}")
        return None


# Example usage
if __name__ == "__main__":
    config = load_configuration_file("config.json")
    print(config)
```

After:

```python
import json
from pathlib import Path


def load_cfg(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)
```

What happened: a missing file or broken JSON now honestly raises an exception the caller can catch where it knows what to do. The comments, docstring, emoji and demo block are gone because they added nothing.

## Go: HTTP handler

Before:

```go
// HandleGetUserRequest handles the HTTP request to get a user by ID.
// It extracts the user ID from the URL, fetches the user from the database,
// and returns the user as JSON.
func (userHandler *UserHandler) HandleGetUserRequest(responseWriter http.ResponseWriter, httpRequest *http.Request) {
	// Extract the user ID from the URL path
	userIDString := httpRequest.PathValue("id")

	// Convert the user ID string to an integer
	userID, conversionError := strconv.Atoi(userIDString)
	if conversionError != nil {
		// Return a bad request error if conversion fails
		http.Error(responseWriter, "Invalid user ID provided. Please provide a valid integer.", http.StatusBadRequest)
		return
	}

	// Fetch the user from the database
	user, fetchError := userHandler.userRepository.GetUserByID(httpRequest.Context(), userID)
	if fetchError != nil {
		log.Printf("Error fetching user: %v", fetchError)
		http.Error(responseWriter, "Internal server error", http.StatusInternalServerError)
		return
	}

	// Set the content type header
	responseWriter.Header().Set("Content-Type", "application/json")
	// Encode the user as JSON and write the response
	json.NewEncoder(responseWriter).Encode(user)
}
```

After:

```go
func (s *Server) user(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.Atoi(r.PathValue("id"))
	if err != nil {
		http.Error(w, "bad id", http.StatusBadRequest)
		return
	}
	u, err := s.db.User(r.Context(), id)
	if err != nil {
		log.Printf("user %d: %v", id, err)
		http.Error(w, "internal error", http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(u)
}
```

## Rust: needless defensiveness

Before:

```rust
/// Calculates the average of a slice of numbers.
///
/// # Arguments
/// * `numbers` - A slice of f64 values
///
/// # Returns
/// The average value, or None if the slice is empty
pub fn calculate_average_value(numbers: &[f64]) -> Option<f64> {
    // Check if the slice is empty
    if numbers.is_empty() {
        return None;
    }
    // Calculate the sum of all numbers
    let total_sum: f64 = numbers.iter().sum();
    // Calculate the count
    let count: usize = numbers.len();
    // Return the average
    Some(total_sum / count as f64)
}
```

After:

```rust
pub fn avg(xs: &[f64]) -> Option<f64> {
    if xs.is_empty() {
        return None;
    }
    Some(xs.iter().sum::<f64>() / xs.len() as f64)
}
```

## A comment worth keeping

```python
# pactl sometimes reports >100% volume and mpris clamps it,
# so clamp here or the slider jumps
vol = min(vol, 1.0)
```

It explains a reason you can't see from the code. That's the kind of comment a human writes — one per screen, not one per line.

## Editing existing code

If asked to "add a retry to `send()`", only `send()` changes. Don't touch the formatting of neighbouring functions, don't add docstrings to code you didn't edit, don't rename variables "for consistency", don't write `# Added retry logic`. The diff should look like it was made by someone who needed a retry — small.
