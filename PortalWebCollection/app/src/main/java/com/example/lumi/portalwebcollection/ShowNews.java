package com.example.lumi.portalwebcollection;


import android.app.*;
import android.content.Intent;
import android.support.v4.app.Fragment;
import android.app.ProgressDialog;
import android.os.Bundle;

import android.support.v4.widget.DrawerLayout;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import com.example.lumi.portalwebcollection.model.New;
import com.example.lumi.portalwebcollection.model.Tag;
import com.example.lumi.portalwebcollection.model.User;
import com.example.lumi.portalwebcollection.util.HttpUtil;
import com.example.lumi.portalwebcollection.util.NewsAdapter;
import com.example.lumi.portalwebcollection.util.Utility;

import org.json.JSONException;
import org.json.JSONObject;
import org.litepal.crud.DataSupport;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.Response;

/**
 * Created by lumi on 2017/11/7.
 */

public class ShowNews extends Fragment {

    private DrawerLayout mDrawerLayout;

    private ProgressDialog progressDialog;
    private Button user;
    private Button hot;
    private Button recommend;
    private Button searchButton;
    private Button search;
    private Button morenews;

    private EditText searchText;

    private ListView listView;
    private ListView typeView;
    private NewsAdapter adapter;
//    private ArrayAdapter<String> adapter;
    private ArrayAdapter<String> adapter2;
    private List<New> dataList = new ArrayList<>();
    private List<String> typeList = new ArrayList<>();

    private List<New> newList;
    private New selectNew;
    private List<User> userList;
    private User current_user;
    private List<Tag> tagList;
    private Tag selectTag;
    private String address;
    private String currentTag;
    private int currentHead;
    private String queryStr;
    private int waitFlag;

    private String[] mVals = {"资讯", "军事", "体育", "娱乐", "时政",
            "国际","财经", "时尚", "汽车","房产","游戏","社会","教育","旅游","科技"};

    public ShowNews() {
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.hot_news, container, false);

        mDrawerLayout = (DrawerLayout) view.findViewById(R.id.drawer_layout);
        mDrawerLayout.setDrawerLockMode(DrawerLayout.LOCK_MODE_LOCKED_CLOSED, Gravity.RIGHT);

        currentHead = 0;

        search = (Button) view.findViewById(R.id.search);
        searchText = (EditText) view.findViewById(R.id.search_text);
        hot = (Button) view.findViewById(R.id.hot_news);
        searchButton = (Button) view.findViewById(R.id.search_button);
        recommend = (Button) view.findViewById(R.id.recommend_news);
        listView = (ListView) view.findViewById(R.id.list_view);
        typeView = (ListView) view.findViewById(R.id.catagory_view);
        user = (Button) view.findViewById(R.id.user);
        morenews = (Button) view.findViewById(R.id.more_news);
        adapter = new NewsAdapter(getContext(), R.layout.news_item, dataList);
        listView.setAdapter(adapter);
        init();

        userList = DataSupport.where("state = ?", String.valueOf(1)).find(User.class);
        if(userList.size() == 0){
            current_user = new User();
            user.setText("登录/注册");
            Log.d("main", String.valueOf(userList.size()));
        }else{
            current_user = userList.get(0);
            user.setText(current_user.getNick_name());
            Log.d("main", current_user.getNick_name());
        }
        return view;
    }

    private void init() {
        tagList = new ArrayList<Tag>();
        for(String i:mVals){
            tagList.add(new Tag(i, i));
            typeList.add(i);
        }

        adapter2 = new ArrayAdapter<>(getContext(), android.R.layout.simple_list_item_1, typeList);
        typeView.setAdapter(adapter2);
    }

    @Override
    public void onActivityCreated( Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);

        mDrawerLayout.setDrawerListener(new DrawerLayout.SimpleDrawerListener() {
            @Override
            public void onDrawerOpened(View drawerView) {
                super.onDrawerOpened(drawerView);
            }

            @Override
            public void onDrawerClosed(View drawerView) {
                super.onDrawerClosed(drawerView);
                mDrawerLayout.setDrawerLockMode(DrawerLayout.LOCK_MODE_LOCKED_CLOSED,
                        Gravity.RIGHT);
            }
        });

        searchButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mDrawerLayout.openDrawer(Gravity.RIGHT);
                mDrawerLayout.setDrawerLockMode(DrawerLayout.LOCK_MODE_UNLOCKED, Gravity.RIGHT);
            }
        });

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener(){
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                selectNew = newList.get(position);

                if(current_user.getUser_name()!= null){
                    send(current_user.getUser_name(), selectNew.getTitle(), selectNew.getUrl());
                }

                Intent intent = new Intent(getContext(), WebView.class);
                intent.putExtra("url", selectNew.getUrl());
                startActivity(intent);

            }
        });

        typeView.setOnItemClickListener(new AdapterView.OnItemClickListener(){
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                morenews.setVisibility(View.VISIBLE);
                hot.setEnabled(true);
                recommend.setEnabled(true);
                selectTag = tagList.get(position);
                Log.d("taggg2323", selectTag.getAddress());
                address = "http://47.95.215.167/news/";
                queryFromServer(address, selectTag.getKind(), 0, 10);
                currentHead = 0;
                currentTag = selectTag.getKind();
                mDrawerLayout.closeDrawer(Gravity.LEFT);
            }
        });

        morenews.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(currentTag.equals("query")){
                    address = "http://47.95.215.167/query/";
                    currentHead += 1;
                    StartSearch(address, queryStr, 0+currentHead*10, 0+currentHead*10+10);
                }else{
                    address = "http://47.95.215.167/news/";
                    currentHead += 1;
                    queryFromServer(address, currentTag, 0+currentHead*10, 0+currentHead*10+10);
                }
            }
        });

        user.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getContext(), UserActivity.class);
                intent.putExtra("user", current_user);
                startActivity(intent);
            }
        });

        hot.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(hot.isEnabled()){
                    hot.setEnabled(false);
                    recommend.setEnabled(true);
                }
                morenews.setVisibility(View.VISIBLE);
                address = "http://47.95.215.167/news/";
                queryFromServer(address, "all", 0, 10);
                currentHead = 0;
            }
        });

        recommend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(current_user.getUser_name() != null){
                    if(recommend.isEnabled()){
                        recommend.setEnabled(false);
                        hot.setEnabled(true);
                    }
                    morenews.setVisibility(View.GONE);
                    address = "http://47.95.215.167/recommend/";
                    queryRecommendFromServer(address, "news");
                }else{
                    Toast.makeText(getActivity(), "请先登录", Toast.LENGTH_SHORT).show();
                }
            }
        });

        search.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                morenews.setVisibility(View.VISIBLE);
                queryStr = searchText.getText().toString();
                Log.d("taggg3232", queryStr);
                address = "http://47.95.215.167/query/";
                mDrawerLayout.closeDrawer(Gravity.RIGHT);
                StartSearch(address, queryStr, 0, 10);
                currentHead = 0;
                currentTag = "query";

            }
        });
        hot.performClick();
    }

    private void queryRecommendFromServer(String address, String news) {
        showProgressDialog();
        JSONObject json = new JSONObject();
        waitFlag = 1;
        try {
            json.put("user_name", current_user.getUser_name());
            HttpUtil.sendOkHttpSession(address,json.toString(), new Callback() {
                @Override
                public void onResponse(Call call, Response response) throws IOException {
                    String responseText = response.body().string();
                    newList = Utility.handleNewResponse(responseText);
                    Log.d("rec", "oasdfaf");
//                    closeProgerssDialog();
                    if(newList != null){
                        Log.d("rec", "ddddd");
                        getActivity().runOnUiThread(new Runnable() {
                            @Override
                            public void run() {

                                dataList.clear();
                                for (New news : newList){
                                    dataList.add(news);
                                    Log.d("rec:", news.getTitle());
                                }
                                adapter.notifyDataSetChanged();
                                listView.setSelection(0);
                                closeProgerssDialog();
                                waitFlag = 0;
                            }
                        });
                    }
                    else
                    {
                        closeProgerssDialog();
                    }
                }

                @Override
                public void onFailure(Call call, IOException e) {
                    getActivity().runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            closeProgerssDialog();
                            waitFlag = 0;
                            Toast.makeText(getContext(), "加载失败", Toast.LENGTH_SHORT).show();
                        }
                    });
                }
            });
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private void send(String user_name, String title, String url) {
        JSONObject json = new JSONObject();
        try {
            json.put("user_name", user_name);
            json.put("title", title);
            json.put("url", url);
            address = "http://47.95.215.167/record/";
            HttpUtil.sendOkHttpSession(address, json.toString(), new Callback() {
                @Override
                public void onFailure(Call call, IOException e) {

                }

                @Override
                public void onResponse(Call call, Response response) throws IOException {

                }
            });
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private void StartSearch(String address, String query, int head, int tail) {
        showProgressDialog();
        JSONObject json = new JSONObject();
        try {
            json.put("query", query);
            json.put("head", head);
            json.put("tail", tail);
            HttpUtil.sendOkHttpPost(address,json.toString(), new Callback() {
                @Override
                public void onResponse(Call call, Response response) throws IOException {
                    String responseText = response.body().string();
                    newList = Utility.handleNewResponse(responseText);
                    Log.d("search", "oasdfaf");
//                    closeProgerssDialog();
                    if(newList != null){
                        Log.d("search", "ddddd");
                        getActivity().runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                dataList.clear();
                                adapter.notifyDataSetChanged();
                                listView.setSelection(0);
                                for (New news : newList){
                                    dataList.add(news);
                                    Log.d("search", news.getTitle());
                                    Log.d("search", news.getImgurl());
                                }
                                adapter.notifyDataSetChanged();
                                listView.setSelection(0);
                                closeProgerssDialog();
                                if(dataList.size() == 0){
                                    morenews.setVisibility(View.GONE);
                                    Toast.makeText(getContext(), "没有了", Toast.LENGTH_SHORT).show();
                                }
                            }
                        });
                    }
                }

                @Override
                public void onFailure(Call call, IOException e) {
                    getActivity().runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            closeProgerssDialog();
                            Toast.makeText(getContext(), "加载失败", Toast.LENGTH_SHORT).show();
                        }
                    });
                }
            });
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private void queryFromServer(String address, final String type, int head, int tail) {
        showProgressDialog();
        JSONObject json = new JSONObject();
        try {
            json.put("kind", type);
            json.put("head", head);
            json.put("tail", tail);
            HttpUtil.sendOkHttpPost(address,json.toString(), new Callback() {
                @Override
                public void onResponse(Call call, Response response) throws IOException {
                    String responseText = response.body().string();
                    newList = Utility.handleNewResponse(responseText);
                    Log.d("query", "6677676");
                    if(newList != null){
                        Log.d("query", "ddddd");
                        getActivity().runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                dataList.clear();
                                adapter.notifyDataSetChanged();
                                listView.setSelection(0);
                                for (New news : newList){
                                    dataList.add(news);
                                    Log.d("query", news.getTitle());
                                }
                                adapter.notifyDataSetChanged();
                                listView.setSelection(0);
                                closeProgerssDialog();
                                if(dataList.size() == 0){
                                    morenews.setVisibility(View.GONE);
                                    Toast.makeText(getContext(), "没有了", Toast.LENGTH_SHORT).show();
                                }
                            }
                        });
                    }else{
                        Log.d("query", "null");
                    }
                }

                @Override
                public void onFailure(Call call, IOException e) {
                    getActivity().runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            closeProgerssDialog();
                            Toast.makeText(getContext(), "加载失败", Toast.LENGTH_SHORT).show();
                        }
                    });
                }
            });

        } catch (JSONException e) {
            e.printStackTrace();
        }

    }

    private void closeProgerssDialog() {
        if(progressDialog != null){
            progressDialog.dismiss();
        }
    }

    private void showProgressDialog() {
        if(progressDialog == null){
            progressDialog = new ProgressDialog(getActivity());
            progressDialog.setMessage("正在加载...");
            progressDialog.setCanceledOnTouchOutside(false);
        }
        progressDialog.show();
    }

}
