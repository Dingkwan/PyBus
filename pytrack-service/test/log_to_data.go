package main

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"pytrack-service/src/config"
	"pytrack-service/src/database"
	"pytrack-service/src/database/table"
	"pytrack-service/src/logger"
	"strconv"
	"strings"
	"time"
)

func main() {
	log := logger.New("test.log", false, true)
	conf := config.Read(log)

	db := database.Connect(conf, log)

	var position []table.Position
	err := filepath.Walk("data", func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if filepath.Ext(path) == ".txt" {
			fmt.Println(path)
			file, err := os.Open(path)
			if err != nil {
				return err
			}
			defer file.Close()

			scanner := bufio.NewScanner(file)
			for scanner.Scan() {
				text := strings.Split(scanner.Text(), ",")
				var (
					taxiId              int64
					longitude, latitude float64
					err                 error
				)

				if taxiId, err = strconv.ParseInt(text[0], 10, 64); err != nil {
					return err
				}
				if longitude, err = strconv.ParseFloat(text[2], 64); err != nil {
					return err
				}
				if latitude, err = strconv.ParseFloat(text[3], 64); err != nil {
					return err
				}

				t, err := time.Parse("2006-01-02 15:04:05", text[1])
				if err != nil {
					return err
				}

				position = append(position, table.Position{
					TaxiID:    taxiId,
					Longitude: longitude,
					Latitude:  latitude,
					Ts:        t.Unix(),
				})
			}
			return nil
		}
		return nil
	})

	if err != nil {
		panic(err)
	}

	fmt.Println(len(position))

	if err = db.CreateInBatches(&position, 1000).Error; err != nil {
		log.Fatal(err.Error())
	}
}
