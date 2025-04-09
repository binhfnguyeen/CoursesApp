import { FlatList, SafeAreaView, Text, Image,TouchableOpacity, View } from "react-native";
import MyStyles from "../../styles/MyStyles";
import { useEffect, useState } from "react";
import { ActivityIndicator, Chip, List } from "react-native-paper";
import Apis, { endpoints } from "../../configs/Apis"
import { useNavigation } from "@react-navigation/native";

const Home = () => {
    const [categories, setCategories] = useState([]);
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(false);

    const loadCates = async () => {
        let res = await Apis.get(endpoints['categories']);
        setCategories(res.data);
    }

    const loadCourses = async () => {
        let url = endpoints['courses'];

        try {
            setLoading(true);
            let res = await Apis.get(url);
            setCourses(res.data.results);
        } catch {

        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadCates();
    }, [])

    useEffect(()=>{
        loadCourses();
    }, [])

    return (
        <SafeAreaView>
            <Text style={[MyStyles.subject, MyStyles.wrap]}>DANH SACH KHOA HOC</Text>

            <View style={MyStyles.row}>
                {categories.map(c => <Chip icon="label" style={MyStyles.m} key={c.id}>{c.name}</Chip>)}
            </View>

            <FlatList 
                ListFooterComponent={loading && <ActivityIndicator />} 
                data={courses} 
                renderItem={({ item }) => (
                    <List.Item 
                        title={item.subject} 
                        description={item.created_date} 
                        left={() => (
                            <TouchableOpacity onPress={() => navigation.navigate('lesson', { "courseId": item.id })}>
                                <Image style={MyStyles.avatar} source={{ uri: item.image }} />
                            </TouchableOpacity>
                        )} 
                    />
                )}
            />
        </SafeAreaView>
    );
}

export default Home;