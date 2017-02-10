
import java.io.*;
import java.util.*;

class GameNode{
    int depth;
    String state, move;
    char currentTurn, opposite;
    GameNode pappa;
    
	public GameNode(int depth, String state, GameNode pappa, String move, char currentTurn){
        this.depth=depth;
        this.state=state;
        this.pappa=pappa;
        this.move=move;
        this.currentTurn=currentTurn;
        if(this.currentTurn=='X')
			this.opposite='O';
		else
			this.opposite='X';
    }
    
	public int get_score(int board[][], int n, char current_player){
        int xValue,oValue;
		xValue=oValue=0;
		for(int i=0; i<n; i++){
            for(int j=0; j<n; j++){
                if(this.state.charAt(i*n+j)=='X')
                    xValue+=board[i][j];
                else if(this.state.charAt(i*n+j)=='O')
                    oValue+=board[i][j];
            }      
        }
        if(current_player=='X')
            return (xValue-oValue);
        else
            return (oValue-xValue);
    }
	
	public ArrayList<GameNode> possibleMoves(int n, int Deep){
		ArrayList<String[]> nextMoves=new ArrayList<String[]>();
		ArrayList<GameNode> childNodes=new ArrayList<GameNode>();
		char turnOpp;
		if(this.currentTurn=='X')
			turnOpp='O';
		else
			turnOpp='X';
		if(this.depth!=Deep){
			for(int i=0;i<n;i++){
				for(int j=0;j<n;j++){
					if(this.state.charAt(n*i+j)=='.'){
						String[] temp=new String[2];
						StringBuilder newString= new StringBuilder(this.state);
						newString.setCharAt(n*i+j,this.currentTurn);
						temp[0]=newString.toString();
						char col=(char)(65+j);
						int row=i+1;
						temp[1]=Character.toString(col)+Integer.toString(row)+" "+"Stake";
						nextMoves.add(temp);
					}
				}
			}
			
			for(int i=0;i<n;i++){
				for(int j=0;j<n;j++){
					String moveType=new String("");
					if(this.state.charAt(n*i+j)=='.'){
						String[] temp=new String[2];
						StringBuilder newString= new StringBuilder(this.state);
						newString.setCharAt(n*i+j,this.currentTurn);
						char col=(char)(65+j);
						int row=i+1;	
						
						if(i-1>=0 && this.state.charAt(n*(i-1)+j)==this.currentTurn)
							moveType="Raid";
						if(j-1>=0 && this.state.charAt((n*i)+j-1)==this.currentTurn)
							moveType="Raid";
						if(j+1<n && this.state.charAt((n*i)+j+1)==this.currentTurn)
							moveType="Raid";
						if(i+1<n && this.state.charAt(n*(i+1)+j)==this.currentTurn)
							moveType="Raid";
						if(moveType=="Raid"){
							if(i-1>=0 && this.state.charAt(n*(i-1)+j)==turnOpp)
								newString.setCharAt(n*(i-1)+j,this.currentTurn);
							if(j-1>=0 && this.state.charAt((n*i)+j-1)==turnOpp)
								newString.setCharAt((n*i)+j-1,this.currentTurn);
							if(j+1<n && this.state.charAt((n*i)+j+1)==turnOpp)
								newString.setCharAt((n*i)+j+1,currentTurn);
							if(i+1<n && this.state.charAt(n*(i+1)+j)==turnOpp)
								newString.setCharAt(n*(i+1)+j,this.currentTurn);
							temp[0]=newString.toString();
							temp[1]=Character.toString(col)+Integer.toString(row)+" "+"Raid";
							nextMoves.add(temp);
						}
					}
				}
			}
			Iterator<String[]> iterator=nextMoves.iterator();
			while(iterator.hasNext()){
				String temp[]=iterator.next();
				GameNode gn=new GameNode(this.depth+1,temp[0],this,temp[1],this.opposite);
				childNodes.add(gn);
			}
		}
		return childNodes;
	}
    
    
    public int findMin(int board[][], char current_player, int Deep, int n){
		ArrayList<GameNode> children= new ArrayList<GameNode>(this.possibleMoves(n, Deep));
        if(this.depth== Deep){
            int v= this.get_score(board, n, current_player);
            return v;
        }
        else{
            int v= Integer.MAX_VALUE;
            Iterator<GameNode> iterator= children.iterator();
            while(iterator.hasNext()){
                GameNode b= iterator.next();
                v=Math.min(v, b.findMax(board, Deep, n, current_player));
            }
            return v;
        }
    }
    
	public int findMax(int board[][], int Deep, int n, char current_player){
        ArrayList<GameNode> children= new ArrayList<GameNode>(this.possibleMoves(n, Deep));
        if(this.depth== Deep){
            int v= this.get_score(board, n, current_player);
			System.out.println(v);
            return v;
        }
        else{
            int v= -Integer.MAX_VALUE;
            Iterator<GameNode> iterator= children.iterator();
            while(iterator.hasNext()){
                GameNode b= iterator.next();
                v=Math.max(v, b.findMin(board, current_player, Deep, n));
            }
            return v;
        }
    }
    
	public String[] miniMax(int n, int Deep, int board[][], char current_player){
        String ans[]= new String[2];
        ArrayList<GameNode> children= new ArrayList<GameNode>(this.possibleMoves(n, Deep));
        Iterator<GameNode> iterator= children.iterator();
        int v=-Integer.MAX_VALUE;
        while(iterator.hasNext()){
			System.out.println("Helloin While");
            GameNode x= iterator.next();
            int i=x.findMin(board, current_player, Deep, n);
            if(v<i){
                ans[0]=x.state;
                ans[1]=x.move;
                v=i;                      
            }
        }
        return ans;
    } 
    
	public String[] AlphaBeta(int n, int Deep, int board[][], char current_player){
        String ans[]= new String[2];
        ArrayList<GameNode> children= new ArrayList<GameNode>(this.possibleMoves(n, Deep));
        Iterator<GameNode> iterator= children.iterator();
        int v=-Integer.MAX_VALUE;
        while(iterator.hasNext()){
            GameNode x= iterator.next();
            int i=x.alphaBetaMin(board, -Integer.MAX_VALUE, Integer.MAX_VALUE, Deep, n, current_player);
            if(v<i){
                ans[0]=x.state;
                ans[1]=x.move;
                v=i;                      
            }
        }
        return ans;
    }
    
	public int alphaBetaMax(int board[][], int alpha, int beta, int Deep, int n, char current_player){
        ArrayList<GameNode> children= new ArrayList<GameNode>(this.possibleMoves(n, Deep));
        if(this.depth==Deep){
            int v= this.get_score(board, n, current_player);
            return v;
        }
        else{
            int v=-Integer.MAX_VALUE;
            Iterator<GameNode> iterator= children.iterator();
            while(iterator.hasNext()){
                GameNode x=iterator.next();
                v=Math.max(v,x.alphaBetaMin(board, alpha, beta, Deep, n, current_player));
                if(v>=beta)
                    return v;
                alpha=Math.max(v,alpha);         
            }
            return v; 
        }    
    }
    
	public int alphaBetaMin(int board[][], int alpha, int beta, int Deep, int n, char current_player){
        ArrayList<GameNode> children= new ArrayList<GameNode>(this.possibleMoves(n, Deep));
        if(this.depth==Deep){
            int v= this.get_score(board, n, current_player);
            return v;
        }
        else{
            int v=Integer.MAX_VALUE;
            Iterator<GameNode> iterator= children.iterator();
            while(iterator.hasNext()){
                GameNode x=iterator.next();
                v=Math.min(v,x.alphaBetaMax(board, alpha, beta, Deep, n, current_player));
                if(v<=alpha)
                    return v;
                beta=Math.min(v,beta);         
            }
            return v; 
        }       
    }
}

public class homework {
	ArrayList<String>data;    
    String ipFile,mode;
	char yourVar;
	int n,level;
	Writer writer;
	GameNode g;
	String boardState="";
	int boardValues[][];
	public void getData()throws Exception{
		BufferedReader in = new BufferedReader(new FileReader("input.txt"));
		data= new ArrayList<String>();
		while((ipFile=in.readLine()) != null){
            data.add(ipFile);
        }
		n=Integer.parseInt(data.get(0));
		mode=data.get(1);
		yourVar=data.get(2).charAt(0);
		level=Integer.parseInt(data.get(3));
		boardValues=new int[n][n];
		for(int i=0;i<n;i++){
			String ipLine[]=data.get(i+4).split(" ");
			for(int j=0;j<n;j++){
				boardValues[i][j]=Integer.parseInt(ipLine[j]);
			}
		}
		for(int i=4+n; i< 4+n+n; i++){
            String ipLine=data.get(i);
            boardState+=ipLine;
        }
		
	}
	
	public void putData()throws Exception{
		writer=new BufferedWriter(new OutputStreamWriter(new FileOutputStream("output.txt"), "utf-8"));
		g=new GameNode(0,boardState,null,"Dummy",yourVar);
		String op[]=new String[2];
		if(mode=="MINIMAX")
			op=g.miniMax(n,level,boardValues,yourVar);
		else
			op=g.AlphaBeta(n,level,boardValues,yourVar);
		writer.write(op[1]+"\n");
		for(int i=0; i<n*n; i+=n){    
			if(i==n*n-1)
                writer.write(op[0].substring(i,i+n));
            else
                writer.write(op[0].substring(i,i+n)+"\n");
        }
		writer.close();
	}
	
	public void checkMaxDepth(){
		int count=0;
		for(int i=0;i<boardState.length();i++){
			if(boardState.charAt(i)=='.')
				count++;
		}
		if (level>count)
			level=count;
	}
	
	public static void main(String args[])throws Exception{
		homework h=new homework();
		h.getData();
		h.checkMaxDepth();
		h.putData();
	}
}