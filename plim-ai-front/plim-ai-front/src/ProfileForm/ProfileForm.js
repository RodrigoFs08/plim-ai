import React, { useState } from 'react';

const ProfileForm = ({ onProfileSubmit }) => {

    const [profileName, setProfileName] = useState('');
    const [video, setVideo] = useState(null);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (profileName && video) {
            onProfileSubmit(profileName, video);
        }
    };

    const handleVideoChange = (e) => {
        setVideo(e.target.files[0]);
    };

    return (
        <form style={{ alignContent: "center" }} onSubmit={handleSubmit}>
            <label style={{ color: 'rgb(240, 240, 245)' }}>
                Insira o Nome do Perfil do Instagram
                <input
                    type="text"
                    style={{ width: '400px', backgroundColor: 'rgb(240, 240, 245)' }}
                    value={profileName}
                    onChange={(e) => setProfileName(e.target.value)}
                />
            </label>
            <label style={{ color: 'rgb(240, 240, 245)' }}>
                Upe o Video
                <input style={{ width: '400px', backgroundColor: 'rgb(240, 240, 245)', color: 'black' }} type="file" accept="video/*" onChange={handleVideoChange} />
            </label>
            <button style={{ width: '100%', fontFamily: 'TheBoldFont' }} type="submit">Enviar Vídeo</button>
        </form>
    );
};
export default ProfileForm;