import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import math


def _draw_chocolate_bar(total_pieces: int, group_size: int):
	"""matplotlib Figure 반환: 가로로 나열된 초콜릿 조각을 그림.
	- total_pieces: 전체 조각 수
	- group_size: 묶음 크기(사용자가 선택한 수)
	묶음이 완전히 나누어지지 않으면 남은 조각은 연한 빨강으로 표시.
	묶음은 반복되는 색 팔레트로 표시한다.
	"""
	# 갈색 계열 팔레트: 각 묶음에 다른 갈색 톤을 사용
	palette = ["#8B4513", "#A0522D", "#D2691E", "#C66A2A", "#7B3F00"]
	fig, ax = plt.subplots(figsize=(6, 1.2))
	ax.set_xlim(0, 1)
	ax.set_ylim(0, 1)
	ax.axis("off")

	if total_pieces <= 0:
		return fig

	# group_size <= 0 이면 아직 후보가 선택되지 않은 초기 상태로 간주
	# 이 경우에는 모든 조각을 동일한 갈색으로 표시하고, 조각 간의 작은 경계선만 보여준다.
	if group_size <= 0:
		piece_w = 1.0 / total_pieces
		base_color = palette[0]
		for i in range(total_pieces):
			x = i * piece_w
			rect = Rectangle((x, 0.15), piece_w, 0.7, facecolor=base_color, edgecolor="black")
			ax.add_patch(rect)
		return fig

	# 묶음별로 블록을 분리해서 그리기: 블록 간에는 작은 간격을 둬서 "떨어진" 효과를 냄
	full_groups = 0 if group_size <= 0 else total_pieces // group_size
	remainder = 0 if group_size <= 0 else total_pieces % group_size

	# 모든 초콜릿 조각 색은 동일한 갈색으로 통일
	base_color = palette[0]

	# 블록 수(완전한 묶음 블록 + 나머지 블록(있다면))
	blocks = full_groups + (1 if remainder > 0 else 0)

	# 블록 간 간격 비율(조각 너비의 비율). 너무 크면 화면을 벗어나므로 0.3 정도로 제한
	gap_factor = 0.4

	if blocks <= 1:
		# 간격 불필요: 기존처럼 균등 분배
		piece_w = 1.0 / total_pieces
		for i in range(total_pieces):
			x = i * piece_w
			# 묶음 안의 조각이면 동일한 갈색, 아니면 잔여 색
			if group_size > 0 and i < full_groups * group_size:
				color = base_color
			else:
				color = "#F7DCDC"
			rect = Rectangle((x, 0.15), piece_w, 0.7, facecolor=color, edgecolor="black")
			ax.add_patch(rect)
	else:
		# gap_factor를 이용해 조각 너비와 gap 너비를 계산
		piece_w = 1.0 / (total_pieces + (blocks - 1) * gap_factor)
		gap_w = gap_factor * piece_w

		x = 0.0
		# 완전한 묶음 블록들 그리기
		for g_idx in range(full_groups):
			for j in range(group_size):
				color = base_color
				rect = Rectangle((x, 0.15), piece_w, 0.7, facecolor=color, edgecolor="black")
				ax.add_patch(rect)
				x += piece_w
			# 블록 끝에는 gap 추가
			x += gap_w

		# 나머지 블록 그리기(있다면)
		if remainder > 0:
			# 남은 조각은 잔여 색으로 표시
			for j in range(remainder):
				color = "#F7DCDC"
				rect = Rectangle((x, 0.15), piece_w, 0.7, facecolor=color, edgecolor="black")
				ax.add_patch(rect)
				x += piece_w

	# 그룹 주위에 테두리를 추가하여 묶음을 강조
	if group_size > 0 and full_groups > 0:
		x = 0.0
		for g_idx in range(full_groups):
			block_w = group_size * piece_w
			ax.add_patch(Rectangle((x, 0.15), block_w, 0.7, fill=False, edgecolor="#333333", linewidth=2))
			x += block_w + gap_w

	return fig


def _status_color(candidate: int, a: int, b: int, g: int):
	"""버튼/상태 색상 결정: 최대공약수->초록, 공약수->노랑, 아니면 빨강"""
	if candidate == g:
		return "#8AE68A"  # 연한 초록
	if a % candidate == 0 and b % candidate == 0:
		return "#FFE66D"  # 노랑
	return "#FF7A7A"  # 빨강


def main():
	st.title("최대공약수(GCD) 시각적 이해")

	st.write("두 숫자를 입력하고 `확인`을 눌러 초콜릿을 생성한 다음, 후보 숫자를 눌러 묶이는 모습을 확인하세요.")

	col1, col2 = st.columns(2)
	with col1:
		a = st.number_input("첫 번째 숫자", min_value=1, max_value=200, value=4, step=1, key="input_a")
	with col2:
		b = st.number_input("두 번째 숫자", min_value=1, max_value=200, value=8, step=1, key="input_b")

	if st.button("확인"):
		st.session_state['n1'] = int(a)
		st.session_state['n2'] = int(b)
		# 새로 입력시 선택 초기화
		st.session_state['selected'] = None

	if 'n1' not in st.session_state:
		st.info("먼저 두 숫자를 입력하고 '확인'을 누르세요.")
		return

	n1 = st.session_state['n1']
	n2 = st.session_state['n2']
	# 후보는 1 .. min(n1, n2)
	max_candidate = min(n1, n2)
	g = math.gcd(n1, n2)

	st.markdown(f"**입력값:** {n1} 과 {n2} — **최대공약수(GCD): {g}**")

	st.write("#### 공약수 후보 (버튼을 눌러 초콜릿 묶임을 확인하세요)")
	# 버튼을 여러 열로 나눠서 보기 좋게 배치
	cols = st.columns(min(10, max_candidate))
	for i in range(1, max_candidate + 1):
		col = cols[(i - 1) % len(cols)]
		color = _status_color(i, n1, n2, g)
		# 버튼을 클릭하면 선택값을 세션에 저장
		if col.button(str(i), key=f"cand_{i}"):
			st.session_state['selected'] = i

		# 버튼 아래에 상태 색상 표시(간단한 색박스)
		col.markdown(f"<div style='width:22px;height:12px;background:{color};border-radius:3px;margin-top:4px'></div>", unsafe_allow_html=True)

	selected = st.session_state.get('selected', None)

	# 선택 상태 안내 (선택이 없어도 초콜릿은 보이도록 함)
	if selected is None:
		st.info("숫자 버튼을 눌러서 초콜릿 묶임을 확인하세요. (선택 없음)")

	# 각 초콜릿 막대 이미지 생성 및 세로(위아래)로 표시
	st.write("#### 초콜릿 시각화")
	# 선택이 없을 때는 group_size=0으로 전체 바를 표시
	draw_size = 0 if selected is None else selected

	st.write(f"{n1}조각 초콜릿")
	fig1 = _draw_chocolate_bar(n1, draw_size)
	st.pyplot(fig1)
	if draw_size > 0:
		full_groups1 = n1 // draw_size
		rem1 = n1 % draw_size
		st.write(f"{draw_size}씩 묶이면: {full_groups1}묶음, 남는 조각: {rem1}")
	else:
		st.write("버튼을 눌러 묶음이 어떻게 나뉘는지 확인해보세요.")

	st.write("---")
	st.write(f"{n2}조각 초콜릿")
	fig2 = _draw_chocolate_bar(n2, draw_size)
	st.pyplot(fig2)
	if draw_size > 0:
		full_groups2 = n2 // draw_size
		rem2 = n2 % draw_size
		st.write(f"{draw_size}씩 묶이면: {full_groups2}묶음, 남는 조각: {rem2}")
	else:
		st.write("버튼을 눌러 묶음이 어떻게 나뉘는지 확인해보세요.")


if __name__ == '__main__':
	main()

