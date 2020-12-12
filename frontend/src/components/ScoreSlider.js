import './Style.css';
import React from 'react';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Nouislider from "nouislider-react";
import "nouislider/distribute/nouislider.css";


export default function ScoreSlider() {
    const Style = {
        padding: '50px 20px',
        color: "rgb(221, 0, 122)",
    };
    
    const Slider = () => (
        <Nouislider 
            id="slider"
            range={{ min: 0, max: 325 }}
            start={321} 
            step={1}
            tooltips={true}
            connect={[true,false]}
            padding={6}
            pips={
                {
                    mode: 'values',
                    values: [0, 100,200,275,325],
                    density: 3
                }
            }
            onSlide={(render, handle, value, un, percent)=>{
                console.log(value);
            }}
            style={{
                Color:"red",
            }}
        />
      );

    return (
        <div>
            <Typography variant="h4" className="block_title" gutterBottom >
                Выбери свою сумму баллов
            </Typography>
            <Paper >
                <div style={Style}>
                    <Slider />
                </div>
            </Paper>
        </div>
    );
}