import os, json

# 도구(Tool): 규칙 기반 심각도 분류
def severity(level):
    if level >= 10: return "High"
    if level >= 7:  return "Medium"
    return "Low"

# 미니 에이전트 실행 함수
def agent_run(alert):
    # ① 인식: 경보에서 필요한 값 추출
    level = alert["level"]
    ip    = alert["ip"]
    rule  = alert["rule"]

    # ② 계획 + ③ 도구 호출: 심각도 분류
    sev = severity(level)

    # 룰 폴백: LLM 키 없이도 동작하는 요약 생성
    llm_key = os.environ.get("LLM_API_KEY")
    if llm_key:
        # 키 있으면 LLM 호출 (여기서는 자리 표시만)
        summary = f"[LLM] IP {ip}에서 {sev} 경보 발생 (rule {rule})"
    else:
        # 룰 폴백: 규칙으로 요약 생성
        summary = f"IP {ip}에서 {sev} 경보 발생 (rule {rule})"

    # ④ 관찰: 결과를 JSON으로 구조화
    report = {
        "ip":       ip,
        "severity": sev,
        "summary":  summary
    }

    # 결과 출력 (값 확인)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report

# 테스트 실행
agent_run({"rule": 5712, "level": 10, "ip": "1.1.1.1"})