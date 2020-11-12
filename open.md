1. 방역당국이 수집서버의 User Table에 '확진자가 다녀간 점포'정보를 질의(방역당국 -> 수집서버)<br/><br/>
   
   * parameters <br/>

        |params|explanation|type|
        |:------:|:-------------:|:---:|
        |userName|User's Name|String|
        |userPhone|User's Phone|String|
    <br/>

    * Response <br/>
      * 확진자가 다녀간 점포들의 서명정보

2. 방역당국이 수집서버의 Owner Table에 '확진자가 다녀간 점포에 방문한 방문자목록'정보를 질의(방역당국 -> 수집서버)<br/><br/>
   
   * parameters <br/>

        |params|explanation|type|
        |:------:|:-------------:|:---:|
        |arrOfA|the array of As|array|
    <br/>

    * Response <br/>
      * 확진자가 다녀간 점포들의 방문자목록