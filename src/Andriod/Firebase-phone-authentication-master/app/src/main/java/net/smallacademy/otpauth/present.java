package net.smallacademy.otpauth;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import android.os.Bundle;
import android.view.MenuItem;

import com.google.android.material.bottomnavigation.BottomNavigationView;

public class present extends AppCompatActivity {


    static String[] header={"Current Prices","'BUY","SELL","Future Pricing"};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_present);


        BottomNavigationView bottomNavigationView=findViewById(R.id.bottom_navigation);
        bottomNavigationView.setOnNavigationItemSelectedListener(navigationItemSelectedListener);


        getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container,new CurrentPriceFragement()).commit();

    }
    private BottomNavigationView.OnNavigationItemSelectedListener navigationItemSelectedListener=new BottomNavigationView.OnNavigationItemSelectedListener() {
        @Override
        public boolean onNavigationItemSelected(@NonNull MenuItem menuItem) {
            Fragment selectedFragement=null;
            switch (menuItem.getItemId()){
                case R.id.current_price:
                    selectedFragement=new CurrentPriceFragement();
                    break;
                case R.id.buy:
                    selectedFragement=new BuyFragement();
                    break;
                case R.id.sell:
                    selectedFragement=new SellFragement();
                    break;
                case R.id.future_price:
                    selectedFragement=new FuturePriceFragement();
                    break;
            }
            getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container,selectedFragement).commit();
            return true;
        }
    };

}
