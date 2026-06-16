import './App.css';

import React, {useEffect, useState} from "react";
import {Button, Input, Label, SearchField} from 'react-aria-components';
import VideoSelector from "./VideoSelector";
import VideoView from "./VideoView";
import ChannelSelector from "./ChannelSelector";
import {useQueries} from "@tanstack/react-query";
import {SearchIcon, MarkGithubIcon, UnmuteIcon} from '@primer/octicons-react'

const retrieveChannels = async () => {
  const response = await fetch('data/channels.json');
  return await response.json();
}

const retrieveChannelVideos = async ({queryKey: [_, channel_id]}) => {
  console.log('channel_id', channel_id);
  const response = await fetch(`data/${channel_id}.json`);
  return await response.json();
};

function App() {
  const [channels, setChannels] = useState(new Map());
  const [searchText, setSearchText] = useState();
  const [selectedChannel, setSelectedChannel] = useState(new Set());
  const [selectedVideos, setSelectedVideos] = useState(new Set());
  const [audioOnly, setAudioOnly] = useState(false);
  const theSearchText = searchText?.trim();


  useEffect(() => {
    const fetchChannels = async () => {
      const resultChannels = await retrieveChannels()
      const channelsMap = new Map(Object.entries(resultChannels))
      setChannels(channelsMap);
      setSelectedChannel(new Set([Array.from(channelsMap.keys())[0]]));
    }
    fetchChannels()
  }, []);

  const results = useQueries({
    queries: Array.from(selectedChannel).map((channel_id) => ({
      queryKey: ['channel_videos', channel_id],
      queryFn: retrieveChannelVideos,
      refetchOnWindowFocus: false,
      enabled: true
    }))
  });

  const videos = results.filter(result => result.isSuccess).flatMap(result => result.data);
  const videosMap = new Map(videos.map(v => [v.video_id, v]));

  let videosList = Array.from(videosMap.values());
  videosList = videosList.filter(v => Array.from(selectedChannel).includes(v.channel_id));
  if (theSearchText) {
    videosList = videosList.filter(v => v.comments.flatMap(c => c.text.toLowerCase()).join().includes(theSearchText.toLowerCase()));
  }
  const theVideo = videosMap.get(selectedVideos.values().next().value);
  return (
    <div style={{margin: "10px 5px"}}>
      <div style={{margin: "5px"}}>
        <div style={{display: "flex", justifyContent: "center", alignItems: "center", gap: "15px"}}>
          <div style={{position: "relative", display: "inline-block", width: "80%"}}>
            <SearchIcon style={{
              position: "absolute",
              left: "10px",
              top: "50%",
              transform: "translateY(-50%)",
              pointerEvents: "none"
            }} />
            <SearchField onChange={setSearchText} onClear={() => setSearchText('')} style={{width: "100%"}}>
              <Input style={{height: "35px", paddingLeft: "36px"}}/>
              <Button>✕</Button>
            </SearchField>
          </div>
          <div>
            <Button
              onClick={() => setAudioOnly(!audioOnly)}
              className={audioOnly ? "positive" : "disabled"}
              style={{
                height: "35px",
                padding: "8px 12px",
                borderRadius: "20px",
                cursor: "pointer",
                fontSize: "14px",
                margin: 0
              }}
            >
              <UnmuteIcon size={16} /> Audio only
            </Button>
          </div>
        </div>
        <ChannelSelector channels={channels} selectedChannel={selectedChannel} setSelectedChannel={setSelectedChannel}/>
      </div>

      <div style={{display: 'flex'}}>
        <VideoSelector videos={videosList} selectedVideos={selectedVideos} handleSelectVideo={setSelectedVideos}/>
        <VideoView key={theVideo?.video_id} video={theVideo} searchText={theSearchText} audioOnly={audioOnly}/>
      </div>

      <div>
        searchText = {theSearchText}<br/>
        selectedVideos = {selectedVideos}<br/>
        selectedChannel = {Array.from(selectedChannel).join(', ')}<br/>
      </div>

      <div style={{marginTop: "20px", textAlign: "center"}}>
        <a href="https://github.com/hoshino-yui/youtubert" target="_blank" rel="noopener noreferrer">
          <MarkGithubIcon size={30} fill="var(--fgColor-default)" />
        </a>
      </div>

      <div style={{marginTop: "5px", textAlign: "center", fontSize: "14px", color: "#555"}}>
        Build Number {document.querySelector('meta[name="build-number"]')?.getAttribute('content')}
      </div>

    </div>

  );
}

export default App;
