package config

import (
	"go.uber.org/zap"
	"gopkg.in/yaml.v2"
	"os"
)

func Read(log *zap.Logger) *Config {
	b, err := os.ReadFile("config.yaml")
	if err != nil {
		log.Fatal(err.Error())
	}

	config := &Config{}

	if err = yaml.Unmarshal(b, config); err != nil {
		log.Fatal(err.Error())
	}

	return config
}
