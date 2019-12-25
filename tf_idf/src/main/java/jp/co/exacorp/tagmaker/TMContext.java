package jp.co.exacorp.tagmaker;

import java.io.File;
import java.io.IOException;
import java.io.Serializable;
import java.util.Collection;
import java.util.TreeSet;

import jp.co.exacorp.tagmaker.copus.Document;
import jp.co.exacorp.tagmaker.copus.Word;
/**
 * <p>タグ作成処理のコンテキストを表すクラス。</p>
 * <p>アプリケーションとUIの境界となるファサードでもある。</p>
 *
 * @author Tasuku Hori
 * (C) Tasuku Hori, exa Corporation Japan, 2017. All rights reserved.
 */
public class TMContext implements Serializable {

	/**
	 * <p>シリアルバージョンUID</p>
	 */
	private static final long serialVersionUID = 3L;

	/**
	 * <p>全単語リストを格納するTSVファイル名</p>
	 */
	public static final String ALL_VOCAB_FILE = "all_vocabs.tsv";

	/**
	 * <p>特徴量評価対象となるキーワードを絞り込んだ単語リストのTSV形式ファイル
	 * （存在しない場合は、全単語リストを使用）</p>
	 */
	public static final String TARGET_VOCAB_FILE = "target_vocabs.tsv";

	/**
	 * <p>全文書シリアライズファイル（このファイルが存在する場合、こちらを先に読む）</p>
	 */
	public static final String ALL_DOC_FILE = "all_docs.ser";

	/**
	 * <p>結果CSVファイル</p>
	 */
	public static final String RESULT_FILE = "result_utf8.csv";

	/**
	 * <p>ソースディレクトリパス</p>
	 */
	private String srcDir = "data" + File.separator + "sample" + File.separator + "src";

	/**
	 * <p>一時ファイル格納ディレクトリパス</p>
	 */
	private String tmpDir = "data" + File.separator + "sample" + File.separator + "tmp";

	/**
	 * <p>結果ファイル格納ディレクトリ</p>
	 */
	private String resultDir = "data" + File.separator + "sample" + File.separator + "result";

	/**
	 * <p>デフォルトコンストラクタ。</p>
	 * <p>各フィールドにはデフォルト値が格納される。</p>
	 */
	public TMContext(){
		FileUtils.evalSrcDir(this.srcDir);
		FileUtils.evalTmpDir(this.tmpDir);
		FileUtils.evalResultDir(resultDir);
	}

	/**
	 * <p>すべてのフィールドを指定可能なコンストラクタ。</p>
	 * @param srcDir ソースディレクトリ
	 * @param tmpDir 一時ファイル格納用ディレクトリ
	 * @param resultDir 結果ファイル格納用ディレクトリ
	 */
	public TMContext(String srcDir, String tmpDir, String resultDir){
		FileUtils.evalSrcDir(srcDir);
		this.srcDir = srcDir;
		FileUtils.evalTmpDir(tmpDir);
		this.tmpDir = tmpDir;
		FileUtils.evalResultDir(resultDir);
		this.resultDir = resultDir;
	}

	/**
	 * <p>ソースディレクトリの格納。</p>
	 * @param srcDir ソースディレクトリ
	 */
	public void setSrcDir(String srcDir){
		FileUtils.evalSrcDir(srcDir);
		this.srcDir = srcDir;
	}

	/**
	 * <p>一時ファイル格納用ディレクトリの格納。</p>
	 * @param tmpDir 一時ファイル格納用ディレクトリ
	 */
	public void setTmpDir(String tmpDir){
		FileUtils.evalTmpDir(tmpDir);
		this.tmpDir = tmpDir;
	}

	/**
	 * <p>結果ファイル格納用ディレクトリの格納。</p>
	 * @param resultDir 結果ファイル格納用ディレクトリ
	 */
	public void setResultDir(String resultDir){
		FileUtils.evalResultDir(resultDir);
		this.resultDir = resultDir;
	}

	/**
	 * <p>結果ファイル格納用ディレクトリの取得。</p>
	 * @return java.lang.String 結果ファイル格納用ディレクトリ
	 */
	public String getResultDir(){
		return this.resultDir;
	}

	/**
	 * <p>全文書リストを取得する。</p>
	 * @return java.util.Collection&lt;jp.co.exacorp.keys.copus.Document&gt; 全文書リスト
	 * @throws java.lang.ClassNotFoundException シリアライズファイル操作中の例外
	 * @throws java.io.IOException ファイル操作中の例外
	 */
	public Collection<Document> getDocuments()
			throws ClassNotFoundException, IOException{
		File file = new File(this.tmpDir + File.separator + ALL_DOC_FILE);
		if(file.isFile() && file.canRead()){
			return FileUtils.loadDocments(this.tmpDir + File.separator + ALL_DOC_FILE);
		}else{
			String[] pathes = FileUtils.getFilePathes(this.srcDir);
			Collection<Document> documents = new TreeSet<Document>();
			for(String path: pathes){
				documents.add(FileUtils.getDocument(path));
			}
			FileUtils.saveDocuments(this.tmpDir + File.separator + ALL_DOC_FILE, documents);
			return documents;
		}
	}

	/**
	 * <p>単語リストを取得する。</p>
	 * @return java.util.Collection&lt;jp.co.exacorp.keys.copus.Word&gt; 全単語リストorキーワード候補単語リスト
	 * @param documents 全文書リスト
	 * @throws java.io.IOException ファイル操作中発生する例外
	 */
	public Collection<Word> getWords(Collection<Document> documents) throws IOException{
		File file = new File(this.tmpDir + File.separator + TARGET_VOCAB_FILE);
		if(file.isFile() && file.canRead()){
			return FileUtils.loadWords(this.tmpDir + File.separator + TARGET_VOCAB_FILE);
		}else{
			Collection<Word> words = CopusUtils.getVocabulary(documents);
			FileUtils.saveWords(this.tmpDir + File.separator + ALL_VOCAB_FILE, words);
			return words;
		}
	}

	/**
	 * <p>TFIDF(t)(d) 値を計算する。</p>
	 * @param documents 全文書リスト
	 * @param words キーワード候補の単語リスト
	 * @return double[][] TFIDF(t)(d)値
	 * @throws java.lang.ClassNotFoundException シリアライズデータ操作中の例外
	 * @throws java.io.IOException ファイル操作中の例外
	 */
	public double[][] compute(Collection<Document> documents, Collection<Word> words)
			throws ClassNotFoundException, IOException{
		// モデル計算
		double[][] result = TFIDFUtils.computeTFIDF(documents, words);
		// 結果保存
		FileUtils.saveResult(resultDir + File.separator + RESULT_FILE, documents, words, result);
		return result;
	}

	/**
	 * <p>フィールド値を表す文字列を返却する。</p>
	 * @return java.lang.String フィールド値を表す文字列
	 */
	@Override
	public String toString(){
		return "srcDir =\t" + this.srcDir + "\ntmpDir =\t" +
				this.tmpDir + "\nresultDir =\t" + this.resultDir;
	}
}
