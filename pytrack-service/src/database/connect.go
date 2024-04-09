package database

import (
	"fmt"
	"go.uber.org/zap"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"pytrack-service/src/config"
	"pytrack-service/src/database/table"
)

func Connect(conf *config.Config, log *zap.Logger) *gorm.DB {
	dsn := fmt.Sprintf("host=%v user=%v password=%v dbname=%v port=%v sslmode=disable TimeZone=Asia/Shanghai",
		conf.Db.Addr, conf.Db.User, conf.Db.Password, conf.Db.Dbname, conf.Db.Port)

	db, err := gorm.Open(postgres.Open(dsn),
		&gorm.Config{
			PrepareStmt: true,
		},
	)

	if err != nil {
		log.Fatal(err.Error())
	}

	if err = db.AutoMigrate(&table.Position{}); err != nil {
		log.Fatal(err.Error())
	}

	return db
}
