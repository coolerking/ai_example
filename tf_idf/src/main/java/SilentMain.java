import java.io.File;
import java.io.IOException;
import java.util.Collection;

import jp.co.exacorp.tagmaker.TMContext;
import jp.co.exacorp.tagmaker.copus.Document;
import jp.co.exacorp.tagmaker.copus.Word;
/**
 * <p>タグ生成処理の引数あり非対話型実行クラス。</p>
 * <p>引数がない場合は、<code>data/sample</code>以下のデータを使って実行します。</p>
 *
 * @author Tasuku Hori
 * (C) Tasuku Hori, exa Corporation Japan, 2017. All right reserved.
 */
public class SilentMain {
	/**
	 * <p>オプション：ソースディレクトリ</p>
	 */
	public static final String ARGPREFIX_SRCDIR = "-s";

	/**
	 * <p>オプション：一時ファイル格納要ディレクトリ</p>
	 */
	public static final String ARGPREFIX_TMPDIR = "-t";

	/**
	 * <p>オプション：結果格納要ディレクトリ</p>
	 */
	public static final String ARGPREFIX_RESULTDIR = "-r";

	/**
	 * <p>非対話型の実行メソッド</p>
	 * <p>コードを読み始めるエントリポイントとなるメソッド。</p>
	 * @param args 引数が格納される
	 * @throws java.lang.ClassNotFoundException シリアライズ操作中の例外
	 * @throws java.io.IOException ファイル操作中の例外
	 */
	public static void main(String[] args) throws ClassNotFoundException, IOException {
		System.out.println("[SilentMain] Start.");
		long elapse = System.currentTimeMillis();

		// コンテキストの生成
		TMContext context = new TMContext();

		if(args!=null && args.length>0){
			try{
				for(int pos=0;pos<args.length;pos++){
					if(args[pos].toLowerCase().startsWith(ARGPREFIX_SRCDIR)){
						context.setSrcDir(args[++pos]);
					}else if(args[pos].toLowerCase().startsWith(ARGPREFIX_TMPDIR)){
						context.setTmpDir(args[++pos]);
					}else if(args[pos].toLowerCase().startsWith(ARGPREFIX_RESULTDIR)){
						context.setResultDir(args[++pos]);
					}
				}
			}catch(RuntimeException re){
				System.err.println("[SilentMain] Illegal arguments!");
				System.err.println("[SilentMain] msg=" + re.getMessage());
				usage();
				throw re;
			}
		}
		System.out.println("[SilentMain] " + context.toString());
		Collection<Document> documents = context.getDocuments();
		Collection<Word> words = context.getWords(documents);
		double[][] tfidf = context.compute(documents, words);

		/**/
		System.out.println("[SilentMain] TFIDF[t][d] result");
		System.out.println();
		for(int t=0;t<tfidf.length; t++){
			for(int d=0;d<tfidf[t].length; d++){
				System.out.print(" ");
				System.out.print(tfidf[t][d]);
			}
			System.out.println();
		}
		/**/
		System.out.println();
		System.out.println("[SilentMain] result file (UTF-8) created at " + context.getResultDir());
		System.out.println("[SilentMain] To convert ShiftJIS file, please \'use nkf -sLw " +
				context.getResultDir() + File.separator + TMContext.RESULT_FILE  + " > result_sjis.csv\'");
		System.out.println("[SilentMain] Done. " + (System.currentTimeMillis() - elapse) + " mSec.");
	}

	/**
	 * <p>使い方を表示する。</p>
	 */
	private static void usage(){
		System.out.print("[USAGE] java SilentMain ");
		System.out.print("[" + ARGPREFIX_SRCDIR + " source_dir_path] ");
		System.out.print("[" + ARGPREFIX_TMPDIR + " temporary_dir_path] ");
		System.out.println("[" + ARGPREFIX_RESULTDIR + " result_dir_path] ");
		System.exit(0);
	}
}
