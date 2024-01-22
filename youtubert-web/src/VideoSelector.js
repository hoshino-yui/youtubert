import React from "react";
import "./VideoSelector.css"
import {ListBox, ListBoxItem} from 'react-aria-components';

function VideoSelector({videos, selectedVideos, handleSelectVideo}) {
  return <ListBox selectionMode="single" selectedKey={selectedVideos} onSelectionChange={handleSelectVideo}>
    {videos.map(video =>
      <ListBoxItem key={video.video_id} id={video.video_id}>
        <div>
          <p className="left-subtitle">{video.channel}</p>
          <p className="right-subtitle">{video.timestamp}</p>
        </div>
        <h4>{video.title}</h4>
      </ListBoxItem>
    )}
  </ListBox>
}

export default VideoSelector;
