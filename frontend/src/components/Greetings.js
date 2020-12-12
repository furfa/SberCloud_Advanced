import './Style.css';
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Divider from '@material-ui/core/Divider';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';




const useStyles = makeStyles((theme) => ({
    root: {
      width: '89%',
    //   maxWidth: '36ch',
      backgroundColor: theme.palette.background.paper,

    },
    inline: {
      display: 'inline',
    },
    large: {
        width: theme.spacing(7),
        height: theme.spacing(7),
      },
  }));

export default function Greetings() {
    const classes = useStyles();

    return (
        <div>
            
            <Typography variant="h4" gutterBottom className="block_title">
                Что мы умеем?
            </Typography>
            <Paper>
                <List className={classes.root}>
                    <ListItem>
                        <ListItemAvatar>
                        <Avatar alt="emoji1" src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/237/smiling-face-with-sunglasses_1f60e.png" 
                            className={classes.large}
                        />
                        </ListItemAvatar>
                        <ListItemText
                        primary="Показывать факультеты, на которые ты можешь пройти"
                        />
                    </ListItem>
                    <Divider variant="inset" component="li" />
                    <ListItem>
                        <ListItemAvatar>
                        <Avatar alt="emoji2" src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/twitter/259/chart-increasing_1f4c8.png" 
                            className={classes.large}
                        />
                        </ListItemAvatar>
                        <ListItemText
                        primary="Показывать динамику изменения балла на последнее бюджетное место"
                        />
                    </ListItem>
                    <Divider variant="inset" component="li" />
                    <ListItem>
                        <ListItemAvatar>
                        <Avatar alt="emoji3" src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/237/male-student_1f468-200d-1f393.png" 
                            className={classes.large}
                        />
                        </ListItemAvatar>
                        <ListItemText
                        primary="Показывать, сколько человек подали документы на другие направления, чтобы ты смог точнее оценить шанс на поступление"
                        />
                    </ListItem>
                </List>
            </Paper>
        </div>
    );
}

