package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
)

func main() {
	log.Print(os.Args)
	r := gin.Default()
	// GET：请求方式；/hello：请求的路径
	// 当客户端以GET方法请求/hello路径时，会执行后面的匿名函数
	r.GET("/hello", func(c *gin.Context) {
		// c.JSON：返回JSON格式的数据
		c.JSON(200, gin.H{
			"message": "Hello world!",
		})
	})

	r.GET("/edm/:filename", FileDownload)

	// 启动HTTP服务，默认在0.0.0.0:8080启动服务
	r.Run(":8088")
	fmt.Printf("Hello word")
}

func fileServer(c *gin.Context) {
	// path:="./go.mod"
	// fileName:=path+c.Query("name")
	c.Header("Content-Type", "application/octet-stream")
	c.Header("Content-Disposition", "attachment; filename="+"2.xlsx")
	c.File("./go.mod")
}
func FileDownload(c *gin.Context) {
	name := c.Param("filename")
	name = name + ".zip"
	pwd, _ := os.Getwd()
	//获取文件或目录相关信息
	fileInfoList, err := ioutil.ReadDir(pwd)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(len(fileInfoList))
	have := false
	for i := range fileInfoList {
		if fileInfoList[i].Name() == name {
			have = true
			break
		} //打印当前文件或目录下的文件或目录名
	}
	if have {
		c.Writer.Header().Add("Content-Disposition", fmt.Sprintf("attachment; filename=%s", "EDMnews.zip")) //fmt.Sprintf("attachment; filename=%s", filename)对下载的文件重命名
		c.Writer.Header().Add("Content-Type", "application/zip")
		c.File("./" + name)
	} else {
		c.String(http.StatusBadRequest, "fail ")
	}

}
