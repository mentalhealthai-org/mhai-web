// src/components/ProfileSidebar.js

import React from 'react';

function AIProfileSideBar({ active }) {
  return (
    <div className="list-group">
      <a
        href="/ai-profile/"
        className={`list-group-item list-group-item-action ${active === 'general' ? 'active' : ''}`}
      >
        General
      </a>
      <a
        href="/ai-profile/interests/"
        className={`list-group-item list-group-item-action ${active === 'interests' ? 'active' : ''}`}
      >
        Interests
      </a>
      <a
        href="/ai-profile/bio/"
        className={`list-group-item list-group-item-action ${active === 'bio' ? 'active' : ''}`}
      >
        Bio
      </a>
      <a
        href="/ai-profile/emotions/"
        className={`list-group-item list-group-item-action ${active === 'emotions' ? 'active' : ''}`}
      >
        Emotions
      </a>
    </div>
  );
}

export default AIProfileSideBar;
