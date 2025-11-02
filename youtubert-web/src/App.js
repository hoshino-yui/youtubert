import './App.css';

import React, {useState} from "react";
import {Button, Input, Label, SearchField} from 'react-aria-components';
import VideoSelector from "./VideoSelector";
import VideoView from "./VideoView";
import ChannelSelector from "./ChannelSelector";
import {useQueries} from "@tanstack/react-query";


function getAllChannels() {
  return new Map(Object.entries({
    'UChAOCCFuF2hto05Z68xp56A': '鈴花ステラ Ch.  Suzuka Stella',
    'UCKiWJEjJw-zGW_Co_kJt5dw': '望月ルーナ  Mochitsugi Luna Ch.',
    'UC5bhpsL8ZUHQ9q-HOLVc82A': 'Cross Ch. 月島クロス【HKVTuber】',
    'UCYPr6jNySMcfpjheFi61U8w': 'Kurona Ch.酒吞玖蘿娜【innoneer.TV】',
    'UCBC7vYFNQoGPupe5NxPG4Bw': 'QuonTama Ch. 久遠たま',
    'UCJcKh9mwJH4zhHsU4NDs54g': 'Rumii Ch. 如月ルミィ【HKVTuber】',
    'UCnwgM2M3C4JOVdOZ0OLu_bA': '小林冰 Aisu Ch.',
    'UCwwvI-bV0CQ4FwkF-Kg0NBQ': '瑠凜紗紀-RuriSaki【HKVtuber】',
    'UCNqQfIrZMLNNJNLB0AOnfAg': '真黑makuro【HKVTuber】',
  }));
}

const retrieveChannelVideos = async ({queryKey: [_, channel_id]}) => {
  console.log('channel_id', channel_id);
  const response = await fetch(`youtubert/data/${channel_id}.json`);
  return await response.json();
};

function App() {
  const channels = getAllChannels();
  const [searchText, setSearchText] = useState();
  const [selectedChannel, setSelectedChannel] = useState(new Set([Array.from(channels.keys())[0]]));
  const [selectedVideos, setSelectedVideos] = useState(new Set());
  const theSearchText = searchText?.trim();

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
