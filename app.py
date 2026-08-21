import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date, timedelta

# 1. Page Configuration
st.set_page_config(
    page_title="모여봐요 약속의 숲 (Streamlit)",
    page_icon="🌲",
    layout="centered",
    initial_sidebar_state="expanded"
)

# File Path for Persistent Storage
DATA_FILE = os.path.join(os.path.dirname(__file__), "polls_data.json")

# Data Persistence Functions (새로운 창/새로고침에서도 영구 보존)
def load_polls_from_file():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_polls_to_file(polls):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(polls, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"저장 중 오류 발생: {e}")

# Load initial data
if "polls" not in st.session_state:
    st.session_state.polls = load_polls_from_file()

if "active_poll_id" not in st.session_state:
    if st.session_state.polls:
        st.session_state.active_poll_id = list(st.session_state.polls.keys())[0]
    else:
        st.session_state.active_poll_id = None

if "temp_dates" not in st.session_state:
    st.session_state.temp_dates = []

# Helper Function: Load Sample Data
def load_sample_data():
    sample_id = "poll_sample_demo"
    st.session_state.polls[sample_id] = {
        "title": "8월 친구들 여름 강원도 여행 🌊",
        "desc": "숙소 예약을 위해 빠르게 날짜 확정합시다!",
        "dates": ["2026-08-28", "2026-08-29", "2026-09-04", "2026-09-05"],
        "voters": [
            {"name": "철수", "votes": {"2026-08-28": "🟢 가능", "2026-08-29": "🟢 가능", "2026-09-04": "🟡 세모", "2026-09-05": "🔴 불가"}},
            {"name": "영희", "votes": {"2026-08-28": "🟢 가능", "2026-08-29": "🟢 가능", "2026-09-04": "🟢 가능", "2026-09-05": "🟢 가능"}},
            {"name": "민수", "votes": {"2026-08-28": "🟢 가능", "2026-08-29": "🟢 가능", "2026-09-04": "🔴 불가", "2026-09-05": "🔴 불가"}},
            {"name": "지은", "votes": {"2026-08-28": "🟡 세모", "2026-08-29": "🟢 가능", "2026-09-04": "🟢 가능", "2026-09-05": "🟡 세모"}}
        ]
    }
    save_polls_to_file(st.session_state.polls)
    st.session_state.active_poll_id = sample_id
    st.toast("샘플 약속 데이터가 불러와졌습니다! 🥳", icon="✨")

# Custom Styling (Glassmorphism & Clean Accent)
st.markdown("""
<style>
    .main { background-color: #0f172a; }
    .winner-box {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(99, 102, 241, 0.15));
        border: 2px solid #f59e0b;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .date-tag {
        display: inline-block;
        background: #334155;
        color: #f8fafc;
        padding: 4px 10px;
        border-radius: 8px;
        margin: 3px;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - Poll Selector & Create
with st.sidebar:
    st.title("🌲 약속의 숲")
    st.caption("Streamlit 개별 날짜 선택 & 영구 저장 지원")

    if st.button("✨ 데모 샘플 데이터 불러오기", use_container_width=True):
        load_sample_data()

    st.divider()

    st.subheader("📁 저장된 약속 목록")
    # Always reload to sync across windows
    st.session_state.polls = load_polls_from_file()
    
    if not st.session_state.polls:
        st.info("등록된 약속이 없습니다. 새 약속을 만들어 보세요!")
    else:
        for p_id, poll in st.session_state.polls.items():
            btn_label = f"📌 {poll['title']}"
            if p_id == st.session_state.active_poll_id:
                btn_label = f"✅ {poll['title']}"
            if st.button(btn_label, key=p_id, use_container_width=True):
                st.session_state.active_poll_id = p_id

# Header Title
st.title("🗓️ 친구들과 약속 날짜 잡기")

# Main Section: Create New Poll OR Manage Selected Poll
tab_create, tab_vote, tab_results = st.tabs(["➕ 새 약속 만들기", "🙋‍♂️ 일정 투표하기", "👑 종합 현황 & 1위 날짜"])

# --- TAB 1: CREATE NEW POLL ---
with tab_create:
    st.subheader("새 약속 투표 만들기")
    
    poll_title = st.text_input("약속 이름 *", placeholder="예: 8월 고교 동창 여름 정모 🍻")
    poll_desc = st.text_input("메모 / 장소 (선택)", placeholder="예: 강남역 부근 / 오후 6시 이후")
    
    st.markdown("#### 📆 후보 날짜 하나씩 선택하기")
    st.caption("달력에서 원하는 날짜를 하나씩 고른 후 **[날짜 추가]** 버튼을 누르거나, 아래 예시 버튼을 클릭하세요!")

    col1, col2 = st.columns([3, 1])
    with col1:
        picked_date = st.date_input("날짜 선택", value=date.today(), min_value=date.today(), key="single_date_picker")
    with col2:
        st.write("") # spacing
        st.write("")
        if st.button("➕ 날짜 추가", use_container_width=True):
            d_str = picked_date.strftime("%Y-%m-%d")
            if d_str not in st.session_state.temp_dates:
                st.session_state.temp_dates.append(d_str)
                st.session_state.temp_dates.sort()
                st.toast(f"{d_str} 날짜가 추가되었습니다!")

    # Quick Select Buttons (주말 빠르게 추가)
    st.caption("⚡ 빠른 추가:")
    q_col1, q_col2, q_col3 = st.columns(3)
    today_date = date.today()
    
    # Next Saturday & Sunday
    next_sat = today_date + timedelta(days=(5 - today_date.weekday()) % 7)
    if next_sat == today_date: next_sat += timedelta(days=7)
    next_sun = next_sat + timedelta(days=1)
    
    with q_col1:
        if st.button(f"이번 주 토 ({next_sat.strftime('%m/%d')})", use_container_width=True):
            d_str = next_sat.strftime("%Y-%m-%d")
            if d_str not in st.session_state.temp_dates:
                st.session_state.temp_dates.append(d_str)
                st.session_state.temp_dates.sort()
    with q_col2:
        if st.button(f"이번 주 일 ({next_sun.strftime('%m/%d')})", use_container_width=True):
            d_str = next_sun.strftime("%Y-%m-%d")
            if d_str not in st.session_state.temp_dates:
                st.session_state.temp_dates.append(d_str)
                st.session_state.temp_dates.sort()
    with q_col3:
        if st.button("🧹 선택 전체 초기화", use_container_width=True):
            st.session_state.temp_dates = []

    # Display Current Selected Dates
    st.markdown("**선택된 후보 날짜 목록:**")
    if not st.session_state.temp_dates:
        st.warning("아직 선택된 날짜가 없습니다. 위에서 날짜를 선택하여 추가해주세요.")
    else:
        tags_html = ""
        for d_str in st.session_state.temp_dates:
            d_obj = datetime.strptime(d_str, "%Y-%m-%d")
            weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][d_obj.weekday()]
            tags_html += f'<span class="date-tag">🗓️ {d_str} ({weekday_kr})</span> '
        st.markdown(tags_html, unsafe_allow_html=True)

    st.divider()

    if st.button("🚀 약속 투표 생성 완료", use_container_width=True, type="primary"):
        if not poll_title.strip():
            st.error("약속 이름을 입력해주세요!")
        elif not st.session_state.temp_dates:
            st.error("최소 1개 이상의 후보 날짜를 추가해주세요!")
        else:
            new_id = f"poll_{int(datetime.now().timestamp())}"
            st.session_state.polls[new_id] = {
                "title": poll_title.strip(),
                "desc": poll_desc.strip(),
                "dates": list(st.session_state.temp_dates),
                "voters": []
            }
            save_polls_to_file(st.session_state.polls)
            st.session_state.active_poll_id = new_id
            st.session_state.temp_dates = [] # Clear temp
            st.success(f"'{poll_title}' 약속 투표가 생성되었습니다! 다른 창이나 친구들도 바로 볼 수 있습니다.")
            st.balloons()
            st.rerun()

# --- CHECK ACTIVE POLL ---
st.session_state.polls = load_polls_from_file() # Ensure fresh data
active_poll = st.session_state.polls.get(st.session_state.active_poll_id)

# --- TAB 2: VOTE FORM ---
with tab_vote:
    if not active_poll:
        st.warning("선택된 약속이 없습니다. 먼저 약속을 생성하거나 왼쪽 사이드바에서 약속을 선택해주세요.")
    else:
        st.subheader(f"📌 {active_poll['title']}")
        if active_poll.get('desc'):
            st.caption(f"💡 {active_poll['desc']}")
        
        st.divider()

        # Voter Selection / Name Input
        voter_names = [v["name"] for v in active_poll["voters"]]
        selected_existing = st.selectbox("투표자 선택 (새 참가자 작성 또는 기존 수정)", ["+ 새 참가자로 작성하기"] + voter_names)
        
        voter_name = ""
        initial_votes = {}
        
        if selected_existing == "+ 새 참가자로 작성하기":
            voter_name = st.text_input("내 이름 입력 *", placeholder="예: 홍길동")
            initial_votes = {d: "🟢 가능" for d in active_poll["dates"]}
        else:
            voter_name = selected_existing
            st.text_input("내 이름 (기존)", value=voter_name, disabled=True)
            existing_voter = next((v for v in active_poll["voters"] if v["name"] == voter_name), None)
            if existing_voter:
                initial_votes = existing_voter["votes"]

        st.markdown("#### 후보 날짜별 가능 여부 선택")
        voted_status = {}

        for d_str in active_poll["dates"]:
            # Format Day of week
            d_obj = datetime.strptime(d_str, "%Y-%m-%d")
            weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][d_obj.weekday()]
            
            cur_val = initial_votes.get(d_str, "🟢 가능")
            val_idx = 0
            if cur_val == "🟡 세모": val_idx = 1
            elif cur_val == "🔴 불가": val_idx = 2

            choice = st.radio(
                f"📅 **{d_str} ({weekday_kr})**",
                ["🟢 가능", "🟡 세모", "🔴 불가"],
                index=val_idx,
                key=f"vote_{st.session_state.active_poll_id}_{d_str}",
                horizontal=True
            )
            voted_status[d_str] = choice

        if st.button("💾 내 일정 제출하기 (자동 저장)", use_container_width=True, type="primary"):
            if not voter_name.strip():
                st.error("이름을 입력해 주세요!")
            else:
                # Update voters list
                voter_entry = {"name": voter_name.strip(), "votes": voted_status}
                idx = next((i for i, v in enumerate(active_poll["voters"]) if v["name"] == voter_name.strip()), None)
                if idx is not None:
                    active_poll["voters"][idx] = voter_entry
                else:
                    active_poll["voters"].append(voter_entry)

                save_polls_to_file(st.session_state.polls)
                st.success(f"{voter_name}님의 투표가 정상적으로 저장되었습니다! 다른 분들도 바로 확인할 수 있습니다.")
                st.balloons()
                st.rerun()

# --- TAB 3: RESULTS & ANALYTICS ---
with tab_results:
    if not active_poll:
        st.warning("선택된 약속이 없습니다.")
    elif not active_poll["voters"]:
        st.info("아직 투표를 제출한 참가자가 없습니다. '일정 투표하기' 탭에서 첫 투표를 시작하세요!")
    else:
        st.subheader(f"📊 {active_poll['title']} - 현황 & 추천 1위")

        # 1. Calculate Scores
        stats = []
        for d_str in active_poll["dates"]:
            avail_cnt = 0
            maybe_cnt = 0
            unavail_cnt = 0
            avail_names = []

            for voter in active_poll["voters"]:
                st_val = voter["votes"].get(d_str, "🟢 가능")
                if st_val == "🟢 가능":
                    avail_cnt += 1
                    avail_names.append(voter["name"])
                elif st_val == "🟡 세모":
                    maybe_cnt += 1
                else:
                    unavail_cnt += 1

            score = (avail_cnt * 2) + (maybe_cnt * 1)
            stats.append({
                "date": d_str,
                "score": score,
                "avail": avail_cnt,
                "maybe": maybe_cnt,
                "unavail": unavail_cnt,
                "avail_names": avail_names
            })

        sorted_stats = sorted(stats, key=lambda x: (x["score"], x["avail"]), reverse=True)
        winner = sorted_stats[0]

        # Winner Box
        d_obj = datetime.strptime(winner["date"], "%Y-%m-%d")
        weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][d_obj.weekday()]

        st.markdown(f"""
        <div class="winner-box">
            <h3 style="color:#f59e0b; margin:0;">👑 가장 최적의 약속 날짜 (1위)</h3>
            <h1 style="color:#ffffff; margin:5px 0;">{winner['date']} ({weekday_kr})</h1>
            <p style="color:#cbd5e1; font-size:16px;">
                참석 가능: <b style="color:#34d399;">{winner['avail']}명</b> ({', '.join(winner['avail_names']) if winner['avail_names'] else '없음'}) 
                {"| 세모: " + str(winner['maybe']) + "명" if winner['maybe'] > 0 else ""}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # 2. DataFrame Matrix
        st.markdown("#### 📋 전체 참가자 투표 매트릭스")
        
        table_data = []
        for d_str in active_poll["dates"]:
            d_obj = datetime.strptime(d_str, "%Y-%m-%d")
            weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][d_obj.weekday()]
            
            row = {"날짜": f"{d_str} ({weekday_kr})"}
            avail_cnt = 0
            for voter in active_poll["voters"]:
                v_vote = voter["votes"].get(d_str, "🟢 가능")
                row[voter["name"]] = v_vote
                if v_vote == "🟢 가능": avail_cnt += 1
            row["가능 인원"] = f"{avail_cnt}명"
            table_data.append(row)

        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)

        # 3. KakaoTalk Share Text Box
        st.markdown("#### 💬 단톡방 공유용 요약 텍스트")
        share_text = f"📢 [{active_poll['title']}] 약속 날짜 투표 현황\n"
        if active_poll.get('desc'):
            share_text += f"📌 {active_poll['desc']}\n"
        share_text += f"👥 총 참여자 ({len(active_poll['voters'])}명): {', '.join([v['name'] for v in active_poll['voters']])}\n\n"
        share_text += f"🏆 [최적 추천 날짜 TOP 3]\n"
        
        for idx, s in enumerate(sorted_stats[:3]):
            d_o = datetime.strptime(s["date"], "%Y-%m-%d")
            w_kr = ["월", "화", "수", "목", "금", "토", "일"][d_o.weekday()]
            share_text += f"{idx+1}위: {s['date']} ({w_kr}) - {s['avail']}명 가능 (참석: {', '.join(s['avail_names']) if s['avail_names'] else '없음'})\n"

        st.code(share_text, language="markdown")
