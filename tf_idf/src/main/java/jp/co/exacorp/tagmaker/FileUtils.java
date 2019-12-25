package jp.co.exacorp.tagmaker;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.util.Collection;
import java.util.Iterator;
import java.util.StringTokenizer;
import java.util.TreeSet;

import jp.co.exacorp.tagmaker.copus.Document;
import jp.co.exacorp.tagmaker.copus.Word;

/**
 * <p>ファイル操作ユーティリティクラス。</p>
 * <p>すべてのメソッドが publicかつstatic定義されており、
 * どのパッケージからも利用可能となっている。</p>
 *
 * @author Tasuku Hori
 * (C) Tasuku Hori, exa Corporation Japan, 2017. All rights reserved.
 */
public class FileUtils {

	/**
	 * <p>分かち書き文書のセパレータ。</p>
	 */
	public static final String WAKATI_SEPARATOR = " ";

	/**
	 * <p>全単語コレクション格納要ファイルのセパレータ。</p>
	 */
	public static final String WORDS_SEPARATOR = "\t";

	/**
	 * <p>結果ファイルのセパレータ。</p>
	 */
	public static final String RESULT_SEPARATOR = ",";

	/**
	 * <p>文書ファイルが格納されているディレクトリパスを評価する。</p>
	 * <p>以下の条件を満たす場合、実行時例外を発生させる。</p>
	 * <ul>
	 * <li> ディレクトリではない</li>
	 * <li> ディレクトリが読めない</li>
	 * <li> ディレクトリ内にサブディレクトリがある</li>
	 * <li> ディレクトリ内にファイルがゼロ</li>
	 * <li> ディレクトリ内のファイルが読めない</li>
	 * </ul>
	 * @param path 対象となるディレくトリパス
	 * @throws java.lang.RuntimeException 妥当性検査に失敗した場合発生
	 */
	public static void evalSrcDir(String path){
		File target = new File(path);
		if(!target.exists()){
			throw new RuntimeException(path + " is not exists!");
		}
		if(!target.isDirectory()){
			throw new RuntimeException(path + " is not a directory path!");
		}
		if(!target.canRead()){
			throw new RuntimeException(path + " can not read!");
		}

		File[] files = target.listFiles();
		if(files==null || files.length==0){
			throw new RuntimeException(path + " has no files inside!");
		}
		for(File file: files){
			if(file.isDirectory()){
				throw new RuntimeException(file.getAbsolutePath() + " is a directory!");
			}
			if(!file.canRead()){
				throw new RuntimeException(file.getAbsolutePath() + " can not read!");
			}
		}
	}

	/**
	 * <p>作業中ファイルを格納するテンポラリディレクトリパスを評価する。</p>
	 * <p>以下の条件を満たす場合実行時例外を発生させる。</p>
	 * <ul>
	 * <li> ディレクトリではない</li>
	 * <li> ディレクトリが読めない</li>
	 * <li> ディレクトリへ書けない</li>
	 * </ul>
	 * @param path 対象となるディレクトリパス
	 * @throws java.lang.RuntimeException 妥当性検査に失敗した場合発生
	 */
	public static void evalTmpDir(String path){
		File target = new File(path);
		if(!target.isDirectory()){
			throw new RuntimeException(path + " is not a directory path!");
		}

		if(!target.canRead()){
			throw new RuntimeException(path + " can not read!");
		}

		if(!target.canWrite()){
			throw new RuntimeException(path + " can not write!");
		}
	}

	/**
	 * <p>結果を格納するディレクトリパスを評価する。</p>
	 * <p>以下の条件を満たす場合実行時例外を発生させる。</p>
	 * <ul>
	 * <li> ディレクトリではない</li>
	 * <li> ディレクトリが読めない</li>
	 * <li> ディレクトリへ書けない</li>
	 * </ul>
	 * @param path 対象となるディレクトリパス
	 * @throws java.lang.RuntimeException 妥当性検査に失敗した場合発生
	 */
	public static void evalResultDir(String path){
		FileUtils.evalTmpDir(path);
	}

	/**
	 * <p>指定したファイルパス先が存在し、読み書き可能かを評価する。</p>
	 * @param path 対象となるファイルパス
	 * @throws java.lang.RuntimeException 妥当性検査に失敗した場合発生
	 */
	public static void evalFilePath(String path){
		File target = new File(path);
		if(!target.isFile()){
			throw new RuntimeException(path + " is not a file!");
		}
		if(!target.canRead()){
			throw new RuntimeException(path + " can not read!");
		}
		if(!target.canWrite()){
			throw new RuntimeException(path + " can not write!");
		}
	}

	/**
	 * <p>文書ファイル(絶対)パス群を取得する。</p>
	 * @param path 文書ファイルが格納されているディレクトリ
	 * @return java.lang.String[] 文書ファオルパス群
	 */
	public static String[] getFilePathes(String path){
		File[] files = new File(path).listFiles();
		String[] pathes = new String[files==null?0:files.length];
		int pos = 0;
		for(File file: files){
			pathes[pos++] = file.getAbsolutePath();
		}
		return pathes;
	}

	/**
	 * <p>文書ファイルから文書インスタンス化する。</p>
	 * @param path ファイルパス
	 * @return jp.co.exacorp.keys.corp.Document 文書インスタンス
	 * @throws java.io.IOException ファイル操作中の例外
	 */
	public static Document getDocument(String path) throws IOException{
		Document document = new Document(path);
		BufferedReader br =
				new BufferedReader(
						new InputStreamReader(
								new FileInputStream(path),"UTF-8"));
		try{
			String line = null;
			while((line = br.readLine())!=null){
				StringTokenizer st = new StringTokenizer(line, WAKATI_SEPARATOR);
				while(st.hasMoreTokens()){
					String text = st.nextToken().trim();
					Word word = document.getWord(text);
					if(word==null) document.setWord(new Word(text));
					else word.setFrequency(word.getFrequency() + 1);
				}
			}
		}finally{
			br.close();
		}
		return document;
	}

	/**
	 * <p>オブジェクトをファイルへ保存する。</p>
	 * @param path 保存先ファイル名
	 * @param target 対象となるオブジェクト
	 * @throws java.io.IOException ファイル操作中の例外
	 */
	public static void saveObject(String path, Object target)
			throws IOException{
		ObjectOutputStream oos =
				new ObjectOutputStream(
						new FileOutputStream(path));
		try{
			oos.writeObject(target);
		}finally{
			oos.close();
		}
	}

	/**
	 * <p>ファイルからオブジェクトを復元する。</p>
	 * @param path 復元元ファイルパス
	 * @return java.lang.Object 復元したオブジェクト
	 * @throws java.lang.ClassNotFoundException 復元したオブジェクトのステレオタイプが異なる場合発生
	 * @throws java.io.IOException ファイル操作中の例外
	 */
	public static Object loadObject(String path)
			throws IOException, ClassNotFoundException{
		ObjectInputStream ois =
				new ObjectInputStream(
						new FileInputStream(path));
		try{
			Object target = ois.readObject();
			return target;
		}finally{
			ois.close();
		}
	}

	/**
	 * <p>全単語コレクションを保存する。</p>
	 * @param path 保存先ファイルパス
	 * @param words 全単語コレクション
	 * @throws java.io.IOException ファイル操作中の例外
	 */
	public static void saveWords(String path, Collection<Word> words)
			throws IOException{
		PrintWriter pw =
				new PrintWriter(
						new BufferedWriter(
								new OutputStreamWriter(
										new FileOutputStream(path),"UTF-8")));
		try{
			for(Word word: words){
				pw.println( word.getText() + WORDS_SEPARATOR +
						new Integer(word.getFrequency()).toString() );
			}
		}finally{
			pw.close();
		}
	}

	/**
	 * <p>全単語コレクションを復元する。</p>
	 * @param path 保存元ファイルパス
	 * @return java.util.Collection&lt;jp.co.exacorp.keys.copus.Word&gt; 全単語コレクション
	 * @throws java.io.IOException ファイル操作中の例外
	 */
	public static Collection<Word> loadWords(String path) throws IOException{
		Collection<Word> words = new TreeSet<Word>();
		BufferedReader br =
				new BufferedReader(
						new InputStreamReader(
								new FileInputStream(path),"UTF-8"));
		try{
			String line = null;
			while((line = br.readLine())!=null){
				StringTokenizer st = new StringTokenizer(line, WORDS_SEPARATOR);
				words.add( new Word(st.nextToken().trim(), Integer.parseInt(st.nextToken())) );
			}
		}finally{
			br.close();
		}
		return words;
	}

	/**
	 * <p>全文書ドキュメントをファイルへ保存する。</p>
	 * @param path 保存先ファイルパス
	 * @param documents 全文書コレクション
	 * @throws java.io.IOException ファイル操作中の例外
	 */
	public static void saveDocuments(String path, Collection<Document> documents)
			throws IOException{
		FileUtils.saveObject(path, documents);
	}

	/**
	 * <p>全文書コレクションを復元する。</p>
	 * @param path 保存元ファイルパス
	 * @return java.util.Collection&lt;jp.co.exacorp.keys.copus.Document&gt; 全文書コレクション
	 * @throws java.io.IOException ファイル操作中の例外
	 * @throws java.lang.ClassNotFoundException オブジェクトのステレオタイプが異なる場合
	 */
	@SuppressWarnings("unchecked")
	public static Collection<Document> loadDocments(String path)
			throws IOException, ClassNotFoundException{
		return (Collection<Document>) FileUtils.loadObject(path);
	}

	/**
	 * <p>最終結果をCSVファイルとして保存する。</p>
	 * @param path 保存先ファイルパス
	 * @param documents 全文書コレクション(横の表題として使用)
	 * @param words 対象とした単語リスト(縦の表題として使用）
	 * @param result TFIDF行列
	 * @throws java.io.IOException ファイル操作中の例外
	 */
	public static void saveResult(String path, Collection<Document> documents,
			Collection<Word> words, double[][] result) throws IOException{
		double[][] target = result;
		PrintWriter pw =
				new PrintWriter(
						new BufferedWriter(
								new OutputStreamWriter(
										new FileOutputStream(path),"UTF-8")));
		try{
			StringBuilder header = new StringBuilder();
			header.append("\"word/document\"");
			for(Document document: documents){
				header.append(RESULT_SEPARATOR);
				header.append("\"");
				header.append(document.getFilePath());
				header.append("\"");
			}
			pw.println(header.toString());

			Iterator<Word> it = words.iterator();
			for(int i=0; i<target.length; i++){
				Word word = it.next();
				StringBuilder line = new StringBuilder();
				line.append("\"");
				line.append(word.getText().trim());
				line.append("\"");
				for(int j=0;j<target[i].length;j++){
					line.append(RESULT_SEPARATOR);
					line.append(new Double(target[i][j]).toString());
				}
				pw.println(line.toString());
			}
		}finally{
			pw.close();
		}
	}

	/**
	 * <p>2次元配列の転置行列を取得する。</p>
	 * @param source 対象となる2次元配列
	 * @return double[][] 転置後の2次元配列
	 */
	public static double[][] transpose(double[][] source){
		double[][] target = new double[source[0].length][source.length];
		for(int i=0;i<target.length; i++){
			for(int j=0;j<target[i].length;j++){
				target[i][j] = source[j][i];
			}
		}

		return target;
	}
}
