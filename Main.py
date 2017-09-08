__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
from ir import IR

def main():
	ir = IR()
	while True:
		query = input('\n請輸入你的問題:')
		print('\n以下為可能回覆的答案:')
		print(ir.find_best_result(query))
		
if __name__ == '__main__':
	main()