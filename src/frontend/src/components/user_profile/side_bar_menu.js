// src/components/ProfileSidebar.js

import React from 'react';

function ProfileSideBar({ active }) {
  return (
    <div className="list-group">
      <a
        href="/profile/"
        className={`list-group-item list-group-item-action ${active === 'general' ? 'active' : ''}`}
      >
        General
      </a>
      <a
        href="/profile/interests/"
        className={`list-group-item list-group-item-action ${active === 'interests' ? 'active' : ''}`}
      >
        Interests
      </a>
      <a
        href="/profile/bio/"
        className={`list-group-item list-group-item-action ${active === 'bio' ? 'active' : ''}`}
      >
        Bio
      </a>
      <a
        href="/profile/emotions/"
        className={`list-group-item list-group-item-action ${active === 'emotions' ? 'active' : ''}`}
      >
        Emotions
      </a>
    </div>
  );
}

export default ProfileSideBar;
