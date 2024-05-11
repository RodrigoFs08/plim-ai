import React, { useState } from 'react';
import ProfileForm from './ProfileForm/ProfileForm';
import ChatInterface from './ChatInterface/ChatInterface';
import LoadingAnimation from './LoadingAnimation/LoadingAnimation';
import './App.css';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [plimAIInstruction, setPlimAIInstruction] = useState('');
  const [hasDescription, setHasDescription] = useState(false);  // Estado para mostrar o chat somente após receber a descrição
  const [isButtonDisabled, setIsButtonDisabled] = useState(false);  // Estado para controlar o botão de enviar no chat

  const handleProfileSubmit = async (profileName, video) => {
    setIsLoading(true);
    const formData = new FormData();
    formData.append('profile_name', profileName);
    formData.append('video', video);

    const response = await fetch('http://127.0.0.1:5000/upload_video_to_plim_ai', {
      method: 'POST',
      body: formData,
    });

    const result = await response.json();
    setMessages([...messages, result.video_description]);
    setPlimAIInstruction(result.plim_ai_instruction);
    setHasDescription(true);  // Habilitar o chat após receber a descrição
    setIsLoading(false);
  };

  const handleSendMessage = async (text) => {
    setIsButtonDisabled(true);  // Desabilitar o botão de enviar enquanto espera a resposta
    setMessages(currentMessages => [...currentMessages, text]);

    const response = await fetch('http://127.0.0.1:5000/plim_ai_chatbot', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt: text, plim_ai_instruction: plimAIInstruction, chat_history: messages }),
    });

    const result = await response.json();
    setMessages(currentMessages => [...currentMessages, result.chat_message]);
    setIsButtonDisabled(false);  // Habilitar o botão de enviar após receber a mensagem
  };

  return (
    <div className="container">
      <div className="card">
        <img src={"https://i.ibb.co/X89LWXs/Whats-App-Image-2024-05-10-at-18-38-41.jpg"} alt="Plim AI Logo" className="logo" />
        {!hasDescription && <ProfileForm onProfileSubmit={handleProfileSubmit} />}
        {isLoading ? <LoadingAnimation /> : hasDescription && <ChatInterface messages={messages} onSend={handleSendMessage} isButtonDisabled={isButtonDisabled} />}
      </div>
    </div>
  );
};

export default App;
