package com.example.lumi.portalwebcollection;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.example.lumi.portalwebcollection.model.User;
import com.example.lumi.portalwebcollection.util.HttpUtil;
import com.example.lumi.portalwebcollection.util.Utility;
import com.zhy.view.flowlayout.TagAdapter;
import com.zhy.view.flowlayout.TagFlowLayout;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Set;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.Response;

public class TagChooseActivity extends AppCompatActivity {

    private String username;
    private String[] mVals = {"资讯", "军事", "体育", "娱乐", "时政",
                    "国际","财经", "时尚", "汽车","房产","游戏","社会","教育","旅游","科技"};
    private TagFlowLayout mFlowLayout;
    private Button chooseButton;
    private Set<Integer> select;
    private List<String> selectTags = new ArrayList<String>();
    private String tags;
    private int Retcode;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //获取布局填充器,一会将tv.xml文件填充到标签内.
        final LayoutInflater mInflater = LayoutInflater.from(this);
        setContentView(R.layout.activity_tag_choose);
        Intent intent = getIntent();
        username = intent.getStringExtra("username");
        Log.d("taggg_tag", username);
        chooseButton = (Button) findViewById(R.id.choose_button);

        for(String i:mVals){
            selectTags.add(i);
        }
        //初始化布局和适配器,直接粘就行.
        mFlowLayout = (TagFlowLayout) findViewById(R.id.id_flowlayout);
        Log.d("taggg45", mVals.toString());
        mFlowLayout.setAdapter(new TagAdapter<String>(mVals)
        {

            @Override
            public View getView(com.zhy.view.flowlayout.FlowLayout parent, int position, String s)
            {
//                将tv.xml文件填充到标签内.
                TextView tv = (TextView) mInflater.inflate(R.layout.tv,
                        mFlowLayout, false);
//               为标签设置对应的内容
                tv.setText(s);
                return tv;
            }
            //             为标签设置预点击内容(就是一开始就处于点击状态的标签)
            @Override
            public boolean setSelected(int position, String s)
            {
                return s.equals("Android");
            }
        });

//          展示哪些标签处于选中状态,这个很重要我们设置标签可点击就是为了把用户选中状态的标签中的数据上传.
        mFlowLayout.setOnSelectListener(new TagFlowLayout.OnSelectListener()
        {
            @Override
            public void onSelected(Set<Integer> selectPosSet)
            {
                setTitle("choose:" + selectPosSet.toString());
//                select.addAll(selectPosSet);
                select = selectPosSet;
//                Collections.copy(select, selectPosSet);
            }
        });

        chooseButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.d("taggg", select.toString());
                tags = "";
                if(select.size()>0){
                    selectTags.clear();
                }
                int flag = 1;
                for(int index : select){
                    selectTags.add(mVals[index]);
                    Log.d("taggg", mVals[index]);
                }

                for (String i:selectTags){
                    if(flag == 1){flag = 0;}
                    else {tags = tags + "/";}
                    tags = tags + i;
                }
//                tags = String.join("/", selectTags);
                Log.d("change_tags", tags);
                sendtags(tags);
                if(Retcode == 0){
                    Intent intent = new Intent(TagChooseActivity.this, MainActivity.class);
                    startActivity(intent);
                }

            }
        });
    }

    private void sendtags(String tags) {
        JSONObject json = new JSONObject();
        try {
            json.put("change_tags", tags);
            json.put("user_name", username);
            String address = "http://47.95.215.167/change_tags/";
            HttpUtil.sendOkHttpSession(address, json.toString(), new Callback() {
                @Override
                public void onFailure(Call call, IOException e) {
                    Log.d("changekinds", "fail");
                    Retcode = -1;
                }

                @Override
                public void onResponse(Call call, Response response) throws IOException {
                    Log.d("changekinds", "tags");
                    String responseText = response.body().string();
                    Retcode = Utility.handleSignResult(responseText);
                }
            });
        } catch (JSONException e) {
            e.printStackTrace();
            Log.d("taggg", e.toString());
        }
    }
}
