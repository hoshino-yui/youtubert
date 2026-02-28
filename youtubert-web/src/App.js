import './App.css';

import React, {useEffect, useState} from "react";
import {Button, Input, Label, SearchField} from 'react-aria-components';
import VideoSelector from "./VideoSelector";
import VideoView from "./VideoView";
import ChannelSelector from "./ChannelSelector";
import {useQueries} from "@tanstack/react-query";


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
    <div style={{margin: "10px"}}>
      <div style={{margin: "5px"}}>
        <div style={{display: "flex", justifyContent: "center"}}>
          <SearchField onChange={setSearchText} onClear={() => setSearchText('')}>
            <Label>Search</Label>
            <Input/>
            <Button>✕</Button>
          </SearchField>
        </div>
        <ChannelSelector channels={channels} selectedChannel={selectedChannel} setSelectedChannel={setSelectedChannel}/>

      </div>
      <div style={{display: 'flex'}}>
        <VideoSelector videos={videosList} selectedVideos={selectedVideos} handleSelectVideo={setSelectedVideos}/>
        <VideoView key={theVideo?.video_id} video={theVideo} searchText={theSearchText}/>
      </div>

      <div>
        searchText = {theSearchText}<br/>
        selectedVideos = {selectedVideos}<br/>
        selectedChannel = {Array.from(selectedChannel).join(', ')}<br/>
      </div>

    </div>

  );
}

export default App;
