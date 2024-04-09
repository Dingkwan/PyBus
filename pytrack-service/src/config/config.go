package config

type Config struct {
	Version float64 `yaml:"version"`
	Db      Db      `yaml:"db"`
}

type Db struct {
	Addr     string `yaml:"addr"`
	Port     string `yaml:"port"`
	Dbname   string `yaml:"dbname"`
	User     string `yaml:"user"`
	Password string `yaml:"password"`
}
