import { View, Text, TouchableOpacity, Image, FlatList } from "react-native";
import MyStyles from "../../styles/MyStyles";
import { ActivityIndicator, List } from "react-native-paper";
import { endpoints } from "../../configs/Apis";
import { useEffect, useState } from "react";
import { useNavigation } from "@react-navigation/native";

const Lessons = ({route}) => {
    const courseId = route.params?.courseId;
    const [lessons, setLessons] = useState([]);
    const [loading, setLoading] = useState(false);
    const nav = useNavigation();
    
    const loadLessons = async () => {
        try {
            setLoading(true);
            let res = await Apis.get(endpoints['lessons'](courseId));
            setLessons(res.data);
        } catch {

        } finally {
            setLoading(false);
        }
    }

    useEffect(()=>{
        loadLessons();
    }, [courseId])

    return (
        <View>
            <FlatList
                ListFooterComponent={loading && <ActivityIndicator />}
                data={lessons}
                renderItem={({ item }) => (
                    <List.Item
                        title={item.subject}
                        description={item.created_date}
                        left={() => (
                            <TouchableOpacity onPress={() => nav.navigate('lesson', { "courseId": item.id })}>
                                <Image style={MyStyles.avatar} source={{ uri: item.image }} />
                            </TouchableOpacity>
                        )}
                    />
                )}
            />
        </View>
    );
}

export default Lessons;