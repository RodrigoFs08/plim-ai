import React, { useState } from 'react';


const ChatInterface = ({ messages, onSend }) => {
    const [message, setMessage] = useState('');

    const sendMessage = (e) => {
        e.preventDefault();
        if (message) {
            onSend(message);
            setMessage('');
        }
    };

    return (
        <div>
            <div style={{ fontFamily: 'Arial', alignContent: "center", height: '300px', width: "400px", borderRadius: '10px', overflowY: 'scroll', border: '1px solid #ccc' }}>
                {messages.map((msg, index) => (
                    <div key={index} style={{ padding: '10px', borderBottom: '1px solid #eee', borderRadius: '5px', color: 'white' }}>
                        {msg}
                    </div>
                ))}
            </div>
            <form onSubmit={sendMessage}>
                <input
                    type="text"
                    value={message}
                    style={{ width: '95%' }}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Digite sua mensagem..."
                />
                <button style={{ fontFamily: 'TheBoldFont' }} type="submit">Enviar Mensagem</button>
            </form>
        </div>
    );
};

export default ChatInterface;
