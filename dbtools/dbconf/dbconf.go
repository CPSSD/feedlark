package dbconf

import (
  "os"
)

func GetURL() string {
  if os.Getenv("ENVIRONMENT") == "PRODUCTION" {
    return "feedlark:hackmeplz@127.0.0.1:9001"
  } else {
    return "127.0.0.1:9001"
  }
}
