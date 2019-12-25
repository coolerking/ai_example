package jp.co.exacorp.common;

import java.io.BufferedReader;
import java.io.InputStreamReader;
/**
 * <p>標準入出力を使った対話型UIユーティリティクラス。</p>
 * <p>対話型CUIを作成する際のユーティリティメソッドを提供する。</p>
 *
 * @author Tasuku Hori
 * (C) Tasuku Hori, exa Corporation Japan, 2017. All rights reserved.
 */
public class StdioUtils {

	/**
	 * <p>終了のためのキー</p>
	 */
	public static final String EXIT = "q";

	/**
	 * <p>数値入力を要求する。</p>
	 * @param msg メッセージ
	 * @return int 入力した数値
	 */
	public static int requireInt(String msg){
        System.out.println(msg);
        System.out.println("type q to quit.");
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        while(true){
        	String buf = "";
        	try{
        		buf = br.readLine();
        		buf = buf==null?"":buf.toLowerCase();
        		if(buf.startsWith(EXIT)){
        			System.out.print("System exited.");
        			System.exit(0);
        		}
        		return Integer.parseInt(buf);
        	}catch(Exception e){
        		System.err.println("Illegal input[" + buf +"], try again!");
                System.out.print(msg);
        	}
        }
	}

	/**
	 * <p>数値入力を要求する。</p>
	 * @return int 入力した数値
	 */
	public static int requireInt(){
		return StdioUtils.requireInt("Input number: ");
	}

	/**
	 * <p>文字入力を要求する。</p>
	 * @param msg メッセージ
	 * @return java.lang.String 入力した文字列
	 */
	public static String requireString(String msg){
        System.out.println(msg);
        System.out.println("type q to quit.");
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        while(true){
        	String buf = "";
        	try{
        		buf = br.readLine();
        		buf = (buf==null)? "":buf;
        		if(buf.toLowerCase().startsWith(EXIT)){
        			System.out.print("System exited.");
        			System.exit(0);
        		}
        		if("".equals(buf.trim())){
        			System.out.print(msg);
        		}else{
        			return buf.trim();
        		}
        	}catch(Exception e){
        		System.err.println("Illegal input[" + buf +"], try again!");
                System.out.print(msg);
        	}
        }
	}

	/**
	 * <p>文字入力を要求する。</p>
	 * @return java.lang.String 入力した文字列
	 */
    public static String requireString(){
    	return StdioUtils.requireString("Input String: ");
    }

    /**
     * <p>メニュー対話型ユーティリティ。</p>
     * @param menus メニューリスト
     * @return int 選択された配列index値
     */
    public static int selectMenu(String[] menus){
    	while(true){
    		System.out.println("----------------------------------------");
    		int pos = 1;
    		for(String menu: menus){
    			System.out.print(pos++);
    			System.out.print(" :");
    			System.out.println(menu);
    		}
    		System.out.println("0 : re-list menu");
    		System.out.println("q : quit");
    		System.out.println("----------------------------------------");
    		int ret = StdioUtils.requireInt();
    		if(ret<0||ret>menus.length){
    			System.err.println("Illegal input!");
    		}else{
    			return ret-1;
    		}
    	}
    }
}
