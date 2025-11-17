import React, { useState } from "react";
import "./App.css";

const BOT = "bot";
const USER = "user";

const initialMessages = [
  {
    id: 1,
    from: BOT,
    text: "안녕하세요, 금융전문비서입니다.\n질문 남겨주시면 친절히 답변해드릴게요!",
  },
];

function App() {
  const [messages, setMessages] = useState(initialMessages);
  const [mode, setMode] = useState(null);
  const [input, setInput] = useState("");

  const addMessage = (msg) => {
    setMessages((prev) => [...prev, { id: Date.now(), ...msg }]);
  };

  const handleBack = () => {
    setMode(null);
    setMessages(initialMessages);
    setInput("");
  };

  const handleClickAdvice = () => {
    setMode("advice");
    addMessage({ from: USER, text: "지금 투자하기 괜찮을까요?" });
    addMessage({
      from: BOT,
      text:
        "현재 시장 상황을 간단히 정리해 드릴게요.\n\n(이 영역은 RAG 연동 예정입니다.)",
    });
  };

  const handleClickProduct = () => {
    setMode("product");
    addMessage({ from: USER, text: "어떤 금융상품이 좋을까요?" });
    addMessage({
      from: BOT,
      text:
        "사용자 정보에 맞는 금융상품을 추천해 드릴게요.\n\n(이 영역은 RAG + 추천 로직 연동 예정입니다.)",
    });
  };

  const handleSend = (e) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) return;
    addMessage({ from: USER, text: trimmed });
    setInput("");
    setTimeout(() => {
      addMessage({
        from: BOT,
        text:
          "현재는 데모 모드입니다.\nRAG 연동 시 실제 금융 데이터를 기반으로 응답이 생성됩니다.",
      });
    }, 400);
  };

  return (
    <div className="app">
      <div className="chat-container">
        {/* 상단 헤더 */}
        <header className="chat-header">
          {mode && (
            <button className="back-btn" onClick={handleBack}>
              ←
            </button>
          )}
          <div className="chat-header-left">
            <div className="chat-avatar">금</div>
            <div>
              <div className="chat-title">금융 AI</div>
              <div className="chat-subtitle">투자 조언 · 상품 추천</div>
            </div>
          </div>
          <span className="chat-status">● online</span>
        </header>

        {/* 채팅 내용 */}
        <main className="chat-main">
          <div className="message-list">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={
                  msg.from === USER
                    ? "message-row message-row-user"
                    : "message-row message-row-bot"
                }
              >
                {msg.from === BOT && <div className="bubble-avatar">AI</div>}
                <div
                  className={
                    msg.from === USER
                      ? "message-bubble bubble-user"
                      : "message-bubble bubble-bot"
                  }
                >
                  {msg.text}
                </div>
              </div>
            ))}

            {/* 투자 조언 카드 */}
            {mode === "advice" && (
              <section className="section-block">
                <p className="section-label">시장 뉴스 (RAG 연동 예정)</p>
                <article className="info-card">
                  <div className="info-card-title">
                    금리 동결 시사, 증시 상승 전망
                  </div>
                  <div className="info-card-body">
                    연준 의장이 금리 인상 종료 가능성을 언급하며 시장에
                    긍정적 신호를 보냈습니다.
                  </div>
                </article>
              </section>
            )}

            {/* 금융상품 추천 카드 */}
            {mode === "product" && (
              <section className="section-block">
                <p className="section-label">
                  추천 금융상품 (RAG + 추천 로직 연동 예정)
                </p>
                <article className="info-card">
                  <div className="info-card-title">청년 혜택 카드</div>
                  <div className="info-card-body">
                    편의점 10% 할인, 교통 5% 할인, 연회비 1만 원대.
                  </div>
                </article>
                <article className="info-card">
                  <div className="info-card-title">목돈 마련 적금</div>
                  <div className="info-card-body">
                    월 30만 원 자동이체, 최대 연 4.0% 금리 제공.
                  </div>
                </article>
              </section>
            )}
          </div>
        </main>

        {/* 입력창 + 선택 버튼 */}
        <footer className="chat-footer">
          {mode === null && (
            <div className="choice-row">
              <button className="choice-card" onClick={handleClickAdvice}>
                📈 투자 조언
              </button>
              <button className="choice-card" onClick={handleClickProduct}>
                💳 금융상품 추천
              </button>
            </div>
          )}
          <form className="chat-input-bar" onSubmit={handleSend}>
            <input
              type="text"
              placeholder="궁금한 점을 물어보세요."
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <button type="submit">전송</button>
          </form>
        </footer>
      </div>
    </div>
  );
}

export default App;
