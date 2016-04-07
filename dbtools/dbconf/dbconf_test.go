package dbconf

import (
  "os"
	"testing"
)

func TestDevelopmentURL(t *testing.T) {
  os.Setenv("ENVIRONMENT", "DEVELOPMENT")
  if GetURL() != "127.0.0.1:9001" {
  	t.Error("Failed to pass TestDevelopmentURL")
  }
}

func TestProductionURL(t *testing.T) {
  os.Setenv("ENVIRONMENT", "PRODUCTION")
  if GetURL() != "feedlark:hackmeplz@127.0.0.1:9001" {
  	t.Error("Failed to pass TestProductionURL")
  }
}
