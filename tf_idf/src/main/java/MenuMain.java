import java.io.File;
import java.io.IOException;
import java.util.Collection;

import jp.co.exacorp.common.StdioUtils;
import jp.co.exacorp.tagmaker.FileUtils;
import jp.co.exacorp.tagmaker.TMContext;
import jp.co.exacorp.tagmaker.copus.Document;
import jp.co.exacorp.tagmaker.copus.Word;
/**
 * <p>タグ生成処理の引数なしCUI対話メニュー型メインクラス。</p>
 * <p>実行すると、標準入力を要求するため、grsadleの実行クラスとして指定しないでください。</p>
 *
 * @author Tasuku Hori
 * (C) Tasuku Hori, exa Corporation Japan, 2017. All rights reserved.
 */
public class MenuMain {


	/**
	 * <p>対話型実行メインメソッド</p>
	 * @param args 使用しない
	 * @throws java.lang.ClassNotFoundException シリアライズデータ使用中の例外
	 * @throws java.io.IOException ファイル操作中の例外
	 */
	public static void main(String[] args) throws ClassNotFoundException, IOException {
		if(args!=null && args.length>0){
			usage();
			System.exit(-1);
		}
		System.out.print("Start keyword percolator with CUI.");
		String srcDir = null;
		while(true){
			srcDir = StdioUtils.requireString("Input source directory path");
			try{
				FileUtils.evalSrcDir(srcDir);
				System.out.println("set source director [" + srcDir + "]");
				break;
			}catch(RuntimeException re){
				System.out.println("Illegal source directory! :" + srcDir);
			}
		}
		String tmpDir = null;
		while(true){
			tmpDir = StdioUtils.requireString("Input temporary directory path");
			try{
				FileUtils.evalTmpDir(tmpDir);
				System.out.println("set temporary director [" + tmpDir + "]");
				break;
			}catch(RuntimeException re){
				System.out.println("Illegal temporary directory! :" + tmpDir);
			}
		}
		String resultDir = null;
		while(true){
			resultDir = StdioUtils.requireString("Input result directory path");
			try{
				FileUtils.evalResultDir(resultDir);
				System.out.println("set result director [" + resultDir + "]");
				break;
			}catch(RuntimeException re){
				System.out.println("Illegal result directory! :" + resultDir);
			}
		}
		TMContext context = new TMContext(srcDir, tmpDir, resultDir);
		System.out.println("Now just ready to start.");
		String ret = null;
		while(true){
			ret = StdioUtils.requireString("Input y/Y or n/N :");
			if(ret.toLowerCase().startsWith("y")) break;
			else{
				System.out.println("Process stopped.");
				System.exit(0);
			}
		}
		Collection<Document> documents = context.getDocuments();
		Collection<Word> words = context.getWords(documents);
		System.out.println("All word TSV file saved file named " + TMContext.ALL_VOCAB_FILE + " in " + tmpDir);
		System.out.println("If you want to eval for selected word you want, please copy it to " +
				tmpDir + File.separator + TMContext.TARGET_VOCAB_FILE);
		System.out.println("Are you ready to continue?.");
		ret = null;
		while(true){
			ret = StdioUtils.requireString("Input y/Y or n/N :");
			if(ret.toLowerCase().startsWith("y")) break;
			else{
				System.out.println("Process stopped.");
				System.exit(0);
			}
		}
		context.compute(documents, words);
		System.out.println("Save result to " + resultDir + File.separator + TMContext.RESULT_FILE);
		System.out.println("Done.");
	}

	/**
	 * <p>使い方表示メソッド。</p>
	 */
	private static void usage(){
		System.out.print("run \'java MenuMain\'!");
	}
}
