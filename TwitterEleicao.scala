import org.apache.spark._
import org.apache.spark.SparkContext._
import org.apache.spark.streaming._
import org.apache.spark.streaming.twitter._
import org.apache.spark.streaming.StreamingContext._
import Utilities._


object TwitterEleicao {
  
  /** Our main function where the action happens */
  def main(args: Array[String]) {

    // Abre o arquivo twitter.txt com as credencias da API
    setupTwitter()
    
    // Define o numero de nucleos que vamos usar
    // Nomeia a aplicacao
    // Define o intervalo de tempo do nosso twitter context, em segundos
    val ssc = new StreamingContext("local[*]", "TwitterEleicao", Seconds(3600))
    
    // Get rid of log spam (should be called after the context is set up)
    setupLogging()

    // Array usado para a filtragem dos Tweets
    val filters = new Array[String](4)
    filters(0) = "bolsonaro"
    filters(1) = "ciro"
    filters(2) = "marina"
    filters(3) = "alckmin"
    
    // Cria a DStream do Twitter using o streaming context
    val tweets = TwitterUtils.createStream(ssc, None, filters).filter(_.getLang == "pt")
    
    // Extrai o texto dos Tweets
    val formatacao = tweets.map(status => status.getText())
    
    // Expressoes regulares para eliminar caracteres especiais, rt e links 
    val formatacao2 = formatacao.map(status => status.replaceAll("""[^a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]""", "").toLowerCase)
    val formatacao3 = formatacao2.map(status => status.replaceAll("""http.*""", ""))
    val formatacao4 = formatacao3.map(status => status.replaceAll("rt ", ""))
    
    // Persistencia agrupando as linhas em uma unica particao
    // Vai gerar um txt para cada janela de tempo definida
    val repartitionedRDD = formatacao4.repartition(1).cache()
    repartitionedRDD.saveAsTextFiles("tweets", "txt")
    
    ssc.start()
    ssc.awaitTermination()
  }  
}